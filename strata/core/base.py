"""Strata 基础层：路径、配置、SQLite 存储。

只做确定性的事：读写文件、建表、存取节点与边。不做任何语义判断。
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "core"
PACKS_DIR = ROOT / "packs"
CARDS_DIR = ROOT / "cards"
DB_PATH = ROOT / "index.sqlite"
GAPS_PATH = ROOT / "gaps.jsonl"

SLOTS = ("intent", "mechanism", "verification", "implementation", "concept")
EDGE_TYPES = ("composed_of", "verified_by", "exercises", "depends_on", "fulfills",
              "explains", "related_to")
STATUSES = ("draft", "proposed", "confirmed", "disputed")
CONFIDENCES = ("certain", "likely", "possible")
SOURCES = ("extractor", "manual", "user-answer", "llm-proposal")

# 槽位对 -> 唯一允许的边类型。用于校验卡片里写的边是否合法。
SLOT_EDGE = {
    ("intent", "mechanism"): "composed_of",
    ("intent", "intent"): "fulfills",
    ("mechanism", "verification"): "verified_by",
    ("verification", "implementation"): "exercises",
    ("implementation", "implementation"): "depends_on",
    # concept 是可选的背景知识层：概念页解释场景/功能点，概念之间互相关联
    ("concept", "intent"): "explains",
    ("concept", "mechanism"): "explains",
    ("concept", "concept"): "related_to",
}

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS node (
  id          TEXT PRIMARY KEY,
  slot        TEXT NOT NULL,
  domain      TEXT NOT NULL,
  title       TEXT NOT NULL,
  status      TEXT NOT NULL,
  confidence  TEXT NOT NULL,
  source      TEXT NOT NULL,
  source_ref  TEXT,
  body        TEXT,
  card_path   TEXT,
  props       TEXT,
  updated_at  TEXT
);
CREATE INDEX IF NOT EXISTS idx_node_slot ON node(slot);
CREATE INDEX IF NOT EXISTS idx_node_domain ON node(domain);

CREATE TABLE IF NOT EXISTS edge (
  src         TEXT NOT NULL,
  dst         TEXT NOT NULL,
  type        TEXT NOT NULL,
  weight      REAL NOT NULL DEFAULT 1.0,
  confidence  TEXT NOT NULL,
  source_type TEXT NOT NULL,
  source_ref  TEXT,
  evidence    TEXT,
  created_at  TEXT,
  PRIMARY KEY (src, dst, type)
);
CREATE INDEX IF NOT EXISTS idx_edge_src ON edge(src);
CREATE INDEX IF NOT EXISTS idx_edge_dst ON edge(dst);
CREATE INDEX IF NOT EXISTS idx_edge_type ON edge(type);

CREATE TABLE IF NOT EXISTS gap (
  id         TEXT PRIMARY KEY,
  hole       TEXT NOT NULL,
  question   TEXT NOT NULL,
  context    TEXT,
  status     TEXT NOT NULL DEFAULT 'open',
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
"""


def now() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


def connect(db_path: Path | str = DB_PATH, reset: bool = False) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.executescript(SCHEMA_SQL)
    if reset:
        conn.executescript("DELETE FROM node; DELETE FROM edge;")
        conn.commit()
    return conn


def connect_readonly(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """只读连接。MCP 服务端只走这条路径。

    多人共用一个服务端时，查询进程绝不能写库：
    - mode=ro 由 SQLite 在文件层拒绝写操作，不依赖调用方自觉；
    - 表不存在于空库时会报错，所以空库直接给出明确提示，而不是静默建表。
    """
    p = Path(db_path)
    if not p.exists():
        raise FileNotFoundError(
            f"索引不存在：{p}\n先在本机跑一次 compile（或让建库的人把 index.sqlite 同步过来）。"
        )
    uri = p.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def append_gap(hole: str, question: str, context: str = "") -> str:
    """把缺口追加进 gaps.jsonl，返回缺口 id。

    jsonl 是缺口的唯一事实源，gap 表只是它的索引。
    这样设计的原因：远端 MCP 服务端是只读打开索引的，
    如果登记缺口必须写库，多用户场景下这条工具就没法用；
    而追加一个文本文件既不需要写权限竞争，也不会把库改坏。
    """
    day = now()[:10].replace("-", "")
    seq = 0
    if GAPS_PATH.exists():
        for line in GAPS_PATH.read_text(encoding="utf-8").splitlines():
            try:
                if json.loads(line).get("id", "").startswith(f"G-{day}-"):
                    seq += 1
            except json.JSONDecodeError:
                continue
    gid = f"G-{day}-{seq + 1:02d}"
    rec = {"id": gid, "hole": hole, "question": question, "context": context,
           "created_at": now()}
    with GAPS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return gid


def replay_gaps(conn: sqlite3.Connection) -> int:
    """把 gaps.jsonl 回放进 gap 表。编译时调用，让缺口不依赖上一次的库状态。

    这里**不提交**：调用方（编译）把整个重建包在一个事务里，
    提前 commit 会让「编到一半失败也不污染旧库」这条保证失效。
    """
    if not GAPS_PATH.exists():
        return 0
    n = 0
    for line in GAPS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        cur = conn.execute(
            "INSERT OR IGNORE INTO gap(id,hole,question,context,status,created_at) "
            "VALUES(?,?,?,?,?,?)",
            (r.get("id"), r.get("hole", "manual"), r.get("question", ""),
             r.get("context", ""), r.get("status", "open"), r.get("created_at", now())),
        )
        n += cur.rowcount
    return n


def load_pack(domain: str) -> dict | None:
    p = PACKS_DIR / domain / "domain.yaml"
    if not p.exists():
        return None
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def list_packs() -> list[str]:
    if not PACKS_DIR.is_dir():
        return []
    return sorted(d.name for d in PACKS_DIR.iterdir() if (d / "domain.yaml").exists())


def allowed_fields(pack: dict | None) -> dict[str, set[str]]:
    """从领域包取出每个槽位允许的业务字段名。"""
    out: dict[str, set[str]] = {}
    if not pack:
        return out
    for slot, spec in (pack.get("slots") or {}).items():
        if isinstance(spec, dict):
            out[slot] = set((spec.get("fields") or {}).keys())
    return out


def slot_label(pack: dict | None, slot: str) -> str:
    if not pack:
        return slot
    spec = (pack.get("slots") or {}).get(slot) or {}
    return spec.get("label") or slot


FM_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$", re.S)


def parse_card(path: Path) -> tuple[dict, str]:
    """切出 frontmatter 与正文。正文里的 --- 不会误伤。"""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        raise ValueError("缺少 frontmatter（文件必须以 --- 开头）")
    fm = yaml.safe_load(m.group(1)) or {}
    if not isinstance(fm, dict):
        raise ValueError("frontmatter 不是映射结构")
    return fm, m.group(2).strip()


def iter_cards(cards_dir: Path | str = CARDS_DIR):
    root = Path(cards_dir)
    if not root.is_dir():
        return
    for p in sorted(root.rglob("*.md")):
        if p.name.startswith("_"):
            continue
        yield p


def dump_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
