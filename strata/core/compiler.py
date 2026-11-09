"""卡片编译：cards/**.md -> index.sqlite。

只做四件事：
  1. 解析 frontmatter
  2. 校验（必填、未知字段、id 重复、槽位合法、边类型与槽位匹配）
  3. 建节点与边
  4. 报悬空 link

任何一条校验失败都只记录、不静默丢弃，最后统一打印。
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from . import base

REQUIRED = ("id", "slot", "domain", "title", "status", "confidence", "source")

# 卡片保留字段，不属于任何领域包的业务字段
RESERVED = {
    "id", "slot", "domain", "title", "status", "confidence", "source",
    "source_ref", "links", "evidence", "tags", "updated", "created",
}

MAX_ERRORS_SHOWN = 40


class Report:
    def __init__(self):
        self.nodes = 0
        self.edges = 0
        self.by_slot: Counter = Counter()
        self.by_confidence: Counter = Counter()
        self.by_domain: Counter = Counter()
        self.by_edge_type: Counter = Counter()
        self.errors: list[dict] = []
        self.warnings: list[dict] = []

    def error(self, card: str, kind: str, detail: str):
        self.errors.append({"card": card, "kind": kind, "detail": detail})

    def warn(self, card: str, kind: str, detail: str):
        self.warnings.append({"card": card, "kind": kind, "detail": detail})

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict:
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "by_slot": dict(self.by_slot),
            "by_confidence": dict(self.by_confidence),
            "by_domain": dict(self.by_domain),
            "by_edge_type": dict(self.by_edge_type),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def compile_cards(cards_dir: Path | None = None, db_path: Path | None = None,
                  verbose: bool = True) -> Report:
    cards_dir = Path(cards_dir or base.CARDS_DIR)
    db_path = Path(db_path or base.DB_PATH)
    rep = Report()

    packs = {pid: base.load_pack(pid) for pid in base.list_packs()}
    fields_by_pack = {pid: base.allowed_fields(p) for pid, p in packs.items()}

    parsed: list[dict] = []
    seen_ids: dict[str, str] = {}

    # ---------- 第一遍：解析 + 单卡校验 ----------
    for path in base.iter_cards(cards_dir):
        rel = path.relative_to(base.ROOT).as_posix() if path.is_relative_to(base.ROOT) else path.name
        try:
            fm, body = base.parse_card(path)
        except Exception as e:
            rep.error(rel, "解析失败", str(e))
            continue

        missing = [k for k in REQUIRED if not fm.get(k)]
        if missing:
            rep.error(rel, "缺少必填字段", ", ".join(missing))
            continue

        slot = str(fm["slot"])
        if slot not in base.SLOTS:
            rep.error(rel, "槽位非法", f"{slot}，允许 {list(base.SLOTS)}")
            continue
        if fm["status"] not in base.STATUSES:
            rep.error(rel, "status 非法", str(fm["status"]))
            continue
        if fm["confidence"] not in base.CONFIDENCES:
            rep.error(rel, "confidence 非法", str(fm["confidence"]))
            continue
        if fm["source"] not in base.SOURCES:
            rep.error(rel, "source 非法", str(fm["source"]))
            continue

        domain = str(fm["domain"])
        if domain not in packs:
            rep.warn(rel, "未知领域包", f"{domain} 未安装，跳过字段校验")

        # 未知字段：防止拼写错误静默失效
        allowed = set(RESERVED)
        allowed |= fields_by_pack.get(domain, {}).get(slot, set())
        unknown = sorted(set(fm) - allowed)
        if unknown:
            rep.error(rel, "未知字段", ", ".join(unknown))
            continue

        nid = str(fm["id"])
        if nid in seen_ids:
            rep.error(rel, "id 重复", f"{nid} 已出现在 {seen_ids[nid]}")
            continue
        seen_ids[nid] = rel

        # 正文过薄检查：知识库的价值在正文（业务知识），只有结构字段等于没写。
        # 只查人工/模型维护的三层，机器抽取的 verification/implementation 不在此列。
        if slot in ("intent", "mechanism", "concept"):
            blen = len((body or "").strip())
            if blen < 60:
                rep.warn(rel, "正文过薄",
                         f"{slot} 卡「{fm['title']}」正文仅 {blen} 字。"
                         f"正文要写背景/触发/流程/边界这些业务知识，"
                         f"只有 frontmatter 的卡片没有检索价值")

        props = {k: v for k, v in fm.items()
                 if k not in RESERVED and k not in ("links", "evidence")}
        links = fm.get("links") or []
        evidence = fm.get("evidence") or []
        if not isinstance(links, list):
            rep.error(rel, "links 结构错误", "必须是列表")
            continue
        if not isinstance(evidence, list):
            evidence = [{"ref": str(evidence), "note": ""}]

        parsed.append({
            "id": nid, "slot": slot, "domain": domain, "title": str(fm["title"]),
            "status": fm["status"], "confidence": fm["confidence"], "source": fm["source"],
            "source_ref": fm.get("source_ref"), "body": body, "card_path": rel,
            "props": props, "links": links, "evidence": evidence, "updated": fm.get("updated"),
        })

    # ---------- 建库 ----------
    # 整个重建放进一个事务：先 DELETE 再 INSERT，中途不提交。
    # 多人共用同一个索引时，读者要么看到旧的完整库，要么看到新的完整库，
    # 绝不会在重编的几十毫秒里查到「0 个节点」。
    conn = base.connect(db_path)
    conn.isolation_level = None
    conn.execute("BEGIN IMMEDIATE")
    conn.execute("DELETE FROM node")
    conn.execute("DELETE FROM edge")
    ts = base.now()
    for n in parsed:
        conn.execute(
            "INSERT INTO node(id,slot,domain,title,status,confidence,source,source_ref,"
            "body,card_path,props,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (n["id"], n["slot"], n["domain"], n["title"], n["status"], n["confidence"],
             n["source"], n["source_ref"], n["body"], n["card_path"],
             base.dump_json(n["props"]), n["updated"] or ts),
        )
        rep.nodes += 1
        rep.by_slot[n["slot"]] += 1
        rep.by_confidence[n["confidence"]] += 1
        rep.by_domain[n["domain"]] += 1

    slot_of = {n["id"]: n["slot"] for n in parsed}
    conf_of = {n["id"]: n["confidence"] for n in parsed}
    merged: dict[tuple, dict] = {}

    # ---------- 第二遍：建边 ----------
    for n in parsed:
        for link in n["links"]:
            if not isinstance(link, dict) or "to" not in link:
                rep.error(n["card_path"], "link 结构错误", str(link))
                continue
            dst = str(link["to"])
            etype = str(link.get("type") or "")
            weight = float(link.get("weight", 1.0))

            if etype not in base.EDGE_TYPES:
                rep.error(n["card_path"], "边类型非法", f"{etype}")
                continue
            if dst not in slot_of:
                rep.error(n["card_path"], "悬空 link", f"{n['id']} -> {dst}（目标卡片不存在）")
                continue

            expect = base.SLOT_EDGE.get((n["slot"], slot_of[dst]))
            if expect is None:
                rep.error(n["card_path"], "槽位不允许连边",
                          f"{n['slot']} -> {slot_of[dst]}（{n['id']} -> {dst}）")
                continue
            if etype != expect:
                rep.error(n["card_path"], "边类型与槽位不符",
                          f"{n['slot']} -> {slot_of[dst]} 应为 {expect}，写了 {etype}")
                continue

            key = (n["id"], dst, etype)
            if key in merged:
                # 同一对节点重复声明：保留高置信度，记一条冲突
                old = merged[key]
                rank = {"certain": 3, "likely": 2, "possible": 1}
                if rank.get(n["confidence"], 0) > rank.get(old["confidence"], 0):
                    merged[key] = {**old, "confidence": n["confidence"],
                                   "source_type": n["source"], "source_ref": n["source_ref"]}
                rep.warn(n["card_path"], "重复声明边", f"{n['id']} ->{etype}-> {dst}")
                continue

            merged[key] = {
                "src": n["id"], "dst": dst, "type": etype, "weight": weight,
                "confidence": n["confidence"], "source_type": n["source"],
                "source_ref": n["source_ref"] or n["card_path"],
                "evidence": n["evidence"],
            }

    for e in merged.values():
        conn.execute(
            "INSERT INTO edge(src,dst,type,weight,confidence,source_type,source_ref,"
            "evidence,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (e["src"], e["dst"], e["type"], e["weight"], e["confidence"],
             e["source_type"], e["source_ref"], base.dump_json(e["evidence"]), ts),
        )
        rep.edges += 1
        rep.by_edge_type[e["type"]] += 1

    # 缺口是 jsonl 派生的：远端只读服务登记的缺口只能落 jsonl，这里统一回放
    base.replay_gaps(conn)

    # 有错误就整体回滚：一份写坏的卡片集不该把共享索引一起拖下水，
    # 读者继续用上一版完整数据，修好卡片再编一次即可。
    if not rep.ok:
        conn.execute("ROLLBACK")
        conn.close()
        if verbose:
            print(render_report(rep))
        return rep

    conn.execute("INSERT OR REPLACE INTO meta(k,v) VALUES('compiled_at',?)", (ts,))
    conn.execute("INSERT OR REPLACE INTO meta(k,v) VALUES('node_count',?)", (str(rep.nodes),))
    conn.execute("COMMIT")
    conn.close()

    if verbose:
        print(render_report(rep))
    return rep


def render_report(rep: Report) -> str:
    L = []
    L.append("=" * 62)
    L.append(f"编译完成  节点 {rep.nodes}  边 {rep.edges}")
    L.append("=" * 62)
    if rep.by_slot:
        L.append("按槽位:   " + "  ".join(f"{k}={v}" for k, v in rep.by_slot.items()))
    if rep.by_edge_type:
        L.append("按边类型: " + "  ".join(f"{k}={v}" for k, v in rep.by_edge_type.items()))
    if rep.by_confidence:
        L.append("按置信度: " + "  ".join(f"{k}={v}" for k, v in rep.by_confidence.items()))
    if rep.by_domain:
        L.append("按领域:   " + "  ".join(f"{k}={v}" for k, v in rep.by_domain.items()))

    if rep.errors:
        L.append("")
        L.append(f"[错误] {len(rep.errors)} 条")
        for e in rep.errors[:MAX_ERRORS_SHOWN]:
            L.append(f"  - {e['card']}  [{e['kind']}]  {e['detail']}")
        if len(rep.errors) > MAX_ERRORS_SHOWN:
            L.append(f"  ... 其余 {len(rep.errors) - MAX_ERRORS_SHOWN} 条省略")
    if rep.warnings:
        L.append("")
        L.append(f"[警告] {len(rep.warnings)} 条")
        for w in rep.warnings[:10]:
            L.append(f"  - {w['card']}  [{w['kind']}]  {w['detail']}")
        if len(rep.warnings) > 10:
            L.append(f"  ... 其余 {len(rep.warnings) - 10} 条省略")
    if not rep.errors and not rep.warnings:
        L.append("")
        L.append("校验通过，无错误无警告。")
    return "\n".join(L)
