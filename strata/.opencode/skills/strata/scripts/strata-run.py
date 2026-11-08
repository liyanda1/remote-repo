#!/usr/bin/env python3
"""Strata skill 的统一入口。

只做三件事：
1. 定位 Strata 工程根（skill 目录可能被复制到任何位置）
2. 把参数原样转发给 strata.py
3. 提供 impact-diff：直接从 git diff 产出影响面，开发者不必自己找符号名

输出全部是纯文本，可以被 OpenCode 的 !`...` 块直接塞进模型上下文。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ENV_HOME = "STRATA_HOME"
HOME_FILE = "strata.home"          # 放在 <你的代码仓>/.opencode/strata.home

USAGE = """strata-run — Strata skill 入口

  strata-run where                     自检：工程根、索引状态、已装领域包
  strata-run next                      告诉我下一步该跑哪条命令（按当前库状态判断）
  strata-run drafts                    列出待确认（draft / proposed）的卡片
  strata-run home [show|set <路径>]     查看/写入工程根位置（避免依赖环境变量）
  strata-run impact-diff [选项]         从 git diff 直接算影响面
      --base <ref>     比较基准，默认 HEAD
      --staged         只看已暂存的改动
      --depth <n>      回溯跳数，默认 4
      --limit <n>      每档最多显示条数，默认 12
  strata-run <其它子命令>               转发给 strata.py（compile/holes/stat/extract/...）

任意子命令都可以带 --home <工程根>，临时指定知识库位置，不写任何配置。
"""

NOT_FOUND = """[strata] 还没指定知识库工程在哪。

三种指定方式，任选一种（优先级从高到低）：

  1. 命令里直接带目录（最省事，不用配置）
       strata-run --home /path/to/strata where

  2. 在当前代码仓写一次配置，之后所有命令都不用再带
       strata-run home set /path/to/strata
     会在 ./.opencode/strata.home 里记下这个路径。

  3. 环境变量（CI / 容器里比较方便）
       export STRATA_HOME=/path/to/strata

工程根的判据：目录下同时存在 strata.py 和 core/。
"""


def is_root(p: Path) -> bool:
    return (p / "strata.py").is_file() and (p / "core").is_dir()


def _read_home_file() -> Path | None:
    """从当前目录向上找 .opencode/strata.home。"""
    cur = Path.cwd().resolve()
    for up in [cur, *cur.parents]:
        f = up / ".opencode" / HOME_FILE
        if f.is_file():
            try:
                p = Path(f.read_text(encoding="utf-8").strip()).expanduser()
            except OSError:
                return None
            # 相对路径按配置文件所在仓根解析，方便整个组用同一个相对位置
            if not p.is_absolute():
                p = (up / p).resolve()
            return p if is_root(p) else None
    return None


def find_root(explicit: str | None = None) -> Path | None:
    """定位工程根。优先级：命令参数 → 仓内配置 → 环境变量 → skill 自身位置 → 当前目录上溯。

    把「命令参数」放第一位，是因为环境和配置都会过期：
    换个仓、换个人、换台机器，配置就指错地方了；命令里带目录永远是对的。
    """
    if explicit:
        p = Path(explicit).expanduser().resolve()
        return p if is_root(p) else None

    from_file = _read_home_file()
    if from_file:
        return from_file

    env = os.environ.get(ENV_HOME)
    if env:
        p = Path(env).expanduser().resolve()
        if is_root(p):
            return p

    here = Path(__file__).resolve()
    for up in here.parents:
        if is_root(up):
            return up

    cur = Path.cwd().resolve()
    for up in [cur, *cur.parents]:
        if is_root(up):
            return up
    return None


def _git(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return 127, "git 未安装"


def _norm(p: str) -> str:
    p = p.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def _same_file(a: str, b: str) -> bool:
    a, b = _norm(a), _norm(b)
    if a == b:
        return True
    return a.endswith("/" + b) or b.endswith("/" + a)


def _diff_hunks(repo: Path, scope: list[str]) -> dict[str, list[tuple[int, int]]]:
    """解析 git diff -U0，得到每个文件被改动的新文件行号区间。

    只按文件匹配会把「改一行注释」放大成「动了文件里所有符号」，
    影响面立刻失去意义，所以必须落到行。
    """
    rc, out = _git(["diff", "-U0", *scope], repo)
    spans: dict[str, list[tuple[int, int]]] = {}
    cur: str | None = None
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:].strip()
            spans.setdefault(cur, [])
        elif line.startswith("+++ /dev/null"):
            cur = None
        elif line.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if not m:
                continue
            start = int(m.group(1))
            count = int(m.group(2)) if m.group(2) is not None else 1
            spans[cur].append((max(1, start - 1), start + count) if count == 0
                              else (start, start + count - 1))
    return spans


def _overlaps(a: int, b: int, spans: list[tuple[int, int]]) -> bool:
    return any(not (b < s or a > e) for s, e in spans)


def cmd_drafts(root: Path) -> int:
    sys.path.insert(0, str(root))
    from core import base  # noqa: E402

    conn = base.connect_readonly()
    rows = conn.execute(
        "SELECT id, slot, title, status, confidence, source, card_path FROM node "
        "WHERE status IN ('draft','proposed') ORDER BY slot, id"
    ).fetchall()
    if not rows:
        print("没有待确认的卡片：所有卡片都已是 confirmed 或 disputed。")
        return 0
    print(f"待确认 {len(rows)} 张（模型产出上限是 proposed，confirmed 只能由人或机器证据给出）")
    print("=" * 62)
    by_slot: dict[str, list] = {}
    for r in rows:
        by_slot.setdefault(r["slot"], []).append(r)
    for slot, items in by_slot.items():
        print(f"\n<{slot}> {len(items)}")
        for r in items:
            print(f"  [{r['status']:<9}] {r['id']}  {r['title'][:36]}  ({r['source']}, {r['confidence']})")
    return 0


def cmd_where(root: Path) -> int:
    sys.path.insert(0, str(root))
    from core import base  # noqa: E402

    print("Strata 自检")
    print("=" * 58)
    print(f"工程根      {root}")
    print(f"入口        {root / 'strata.py'}")
    print(f"索引        {base.DB_PATH}  {'存在' if base.DB_PATH.exists() else '不存在'}")

    cards = list(base.CARDS_DIR.rglob("*.md")) if base.CARDS_DIR.is_dir() else []
    print(f"卡片文件    {len(cards)}")

    packs = base.list_packs()
    print(f"领域包      {', '.join(packs) if packs else '（无）'}")

    if base.DB_PATH.exists():
        conn = base.connect_readonly()
        n = conn.execute("SELECT COUNT(*) c FROM node").fetchone()["c"]
        e = conn.execute("SELECT COUNT(*) c FROM edge").fetchone()["c"]
        g = conn.execute("SELECT COUNT(*) c FROM gap WHERE status='open'").fetchone()["c"]
        print(f"节点 / 边   {n} / {e}")
        print(f"未闭合缺口  {g}")
        if n == 0:
            print("\n索引是空的：先跑 strata-run extract <repo>，再跑 strata-run compile")
    else:
        print("\n还没有索引：先跑 strata-run extract <repo>，再跑 strata-run compile")
    return 0


def cmd_home(argv: list[str]) -> int:
    """查看 / 写入工程根位置。写入后所有命令都不用再带目录。"""
    action = argv[0] if argv else "show"
    if action == "set":
        if len(argv) < 2:
            print("用法：strata-run home set <工程根路径>")
            return 2
        p = Path(argv[1]).expanduser().resolve()
        if not is_root(p):
            print(f"拒绝：{p} 不像工程根（需要有 strata.py 和 core/）。")
            return 2
        target = Path.cwd() / ".opencode"
        target.mkdir(parents=True, exist_ok=True)
        f = target / HOME_FILE
        f.write_text(str(p) + "\n", encoding="utf-8")
        print(f"已记录：{f}")
        print(f"指向    ：{p}")
        print("之后所有命令都不用再带 --home，也不用设环境变量。")
        return 0

    # show：把每条候选来源都列出来，指错地方时一眼能看出是哪一层生效
    print("工程根定位")
    print("=" * 58)
    f = None
    cur = Path.cwd().resolve()
    for up in [cur, *cur.parents]:
        if (up / ".opencode" / HOME_FILE).is_file():
            f = up / ".opencode" / HOME_FILE
            break
    print(f"仓内配置    {f if f else '（无）'}")
    print(f"环境变量    {os.environ.get(ENV_HOME) or '（未设置）'}")
    here = Path(__file__).resolve()
    up_hit = next((u for u in here.parents if is_root(u)), None)
    print(f"skill 位置  {up_hit if up_hit else '（不在工程内）'}")
    root = find_root()
    print("-" * 58)
    print(f"最终生效    {root if root else '（没找到，用 home set 指定）'}")
    return 0 if root else 2


def cmd_next(root: Path) -> int:
    """按当前库状态判断下一步该跑哪条命令。

    存在的意义：命令是链式的，但人不该记住这条链。
    任何一步做完都调它一次，输出直接告诉用户下一条命令是什么、为什么。
    """
    sys.path.insert(0, str(root))
    from core import analyze, base  # noqa: E402

    if not base.DB_PATH.exists():
        print("状态：还没有索引")
        print("下一步：/strata-init")
        print("原因：index.sqlite 不存在，先抽取代码并编译。")
        print("说明：它会跑 extract → compile，然后带你播第一批场景卡。")
        return 0

    conn = base.connect_readonly(base.DB_PATH)
    counts = {r["slot"]: r["c"] for r in
              conn.execute("SELECT slot, COUNT(*) c FROM node GROUP BY slot").fetchall()}
    total = sum(counts.values())
    drafts = {r["slot"]: r["c"] for r in conn.execute(
        "SELECT slot, COUNT(*) c FROM node WHERE status IN ('draft','proposed') "
        "GROUP BY slot").fetchall()}
    n_draft = sum(drafts.values())
    holes = {h["hole"]: h["count"] for h in analyze.find_holes(conn, 1)}

    print("当前状态")
    print("=" * 58)
    print("  " + "  ".join(f"{k}={counts.get(k, 0)}" for k in base.SLOTS) + f"  合计 {total}")
    if n_draft:
        print("  待裁决 " + "  ".join(f"{k}={v}" for k, v in drafts.items()))
    print()

    def say(cmd: str, why: str, then: str = "") -> None:
        print(f"下一步：{cmd}")
        print(f"原因  ：{why}")
        if then:
            print(f"之后  ：{then}")

    if total == 0:
        say("/strata-init", "索引是空的。", "跑完后会告诉你选哪份文档播种场景。")
        return 0

    if counts.get("intent", 0) == 0:
        say("/strata-init", "代码层已经有了，但场景层还是空的——没有 intent 就没有业务轴。",
            "播完 intent 卡再 /strata-review 裁决。")
        return 0

    if n_draft:
        slots = "、".join(f"{k} {v} 张" for k, v in drafts.items())
        say("/strata-review", f"有 {n_draft} 张草稿没裁决（{slots}）。",
            "/strata-fill 补结构空洞。")
        return 0

    if holes.get("H4-unsourced-edge", 0):
        say("/strata-fill", f"有 {holes['H4-unsourced-edge']} 条边没有证据来源，这是致命级空洞。",
            "补完再看其它空洞。")
        return 0

    rest = {k: v for k, v in holes.items() if v and k != "H4-unsourced-edge"}
    if rest:
        top = max(rest.items(), key=lambda kv: kv[1])
        say("/strata-fill", f"剩下 {sum(rest.values())} 处空洞，最多的是 {top[0]}（{top[1]} 处）。",
            "空洞清到可接受范围后，日常就用 /strata-impact。")
        return 0

    say("/strata-impact", "库是健康的：没有待裁决草稿，也没有结构空洞。",
        "改代码前跑它；想看整体状况用 /strata-status。")
    return 0


def cmd_impact_diff(root: Path, argv: list[str]) -> int:
    base_ref, staged, depth, limit = "HEAD", False, 4, 12
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--base" and i + 1 < len(argv):
            base_ref = argv[i + 1]; i += 2
        elif a == "--staged":
            staged = True; i += 1
        elif a == "--depth" and i + 1 < len(argv):
            depth = int(argv[i + 1]); i += 2
        elif a == "--limit" and i + 1 < len(argv):
            limit = int(argv[i + 1]); i += 2
        else:
            i += 1

    rc, out = _git(["rev-parse", "--show-toplevel"], Path.cwd())
    if rc != 0:
        print("[strata] 当前目录不在 git 仓库内，无法读取改动。")
        print("提示：在代码仓根目录执行，或手动传入符号名用 strata-run impact <符号>。")
        return 2
    repo = Path(out.strip().splitlines()[0])

    scope = ["--diff-filter=ACMR"] + (["--cached"] if staged else [base_ref])
    rc, out = _git(["diff", "--name-only", *scope], repo)
    files = [l.strip() for l in out.splitlines() if l.strip()]
    if not files:
        print(f"没有检出改动（基准 {base_ref}{'，已暂存' if staged else ''}）。")
        return 0

    hunks = _diff_hunks(repo, scope)

    sys.path.insert(0, str(root))
    import json

    from core import analyze, base  # noqa: E402

    def spans_of(path: str) -> list[tuple[int, int]]:
        for k, v in hunks.items():
            if _same_file(k, path):
                return v
        return []

    conn = base.connect_readonly()
    rows = conn.execute(
        "SELECT id, slot, title, props, source_ref FROM node "
        "WHERE slot IN ('implementation','mechanism')"
    ).fetchall()

    hit: dict[str, list[dict]] = {f: [] for f in files}
    fallback: dict[str, list[dict]] = {f: [] for f in files}
    for r in rows:
        props = json.loads(r["props"] or "{}")
        locs = props.get("locations") or []
        if not locs:
            f0 = props.get("file") or props.get("header")
            if not f0:
                continue
            if props.get("line") is None:
                locs = [{"file": f0, "line": None}]      # 模块节点：没有行号
            else:
                locs = [{"file": f0, "line": props["line"],
                         "line_end": props.get("line_end") or props["line"]}]
        for loc in locs:
            f, ln = loc.get("file"), loc.get("line")
            le = loc.get("line_end") or ln
            for cf in files:
                if not _same_file(f, cf):
                    continue
                item = {"id": r["id"], "slot": r["slot"], "title": r["title"],
                        "file": f, "ref": r["source_ref"], "line": ln, "line_end": le}
                if ln is None or not spans_of(cf):
                    # 模块节点没有行号，或改动落在符号之外（宏、注释、include）
                    fallback[cf].append(item)
                elif _overlaps(int(ln), int(le), spans_of(cf)):
                    hit[cf].append(item)

    # 该文件已经有符号级命中时，模块级回退是冗余信息，去掉以免混淆
    for cf in files:
        if hit[cf]:
            fallback[cf] = []

    matched = [s for v in hit.values() for s in v]
    fb = [s for v in fallback.values() for s in v]
    empty = [f for f in files if not hit[f] and not fallback[f]]

    print("Strata 影响面 · 基于 git diff")
    print("=" * 62)
    print(f"仓库      {repo}")
    print(f"基准      {base_ref}{'（已暂存）' if staged else ''}")
    print(f"改动文件  {len(files)} 个，命中知识库符号 {len(matched)} 个")

    if matched:
        print("\n■ 改动点（按行范围定位）")
        for s in matched[:20]:
            rng = f":{s['line']}-{s['line_end']}" if s["line"] else ""
            print(f"  [{s['slot'][:4]}] {s['id']}  {s['file']}{rng}")
        if len(matched) > 20:
            print(f"  … 其余 {len(matched) - 20} 个")

    if fb:
        print("\n■ 文件级回退（改动不落在任何已知符号的范围内）")
        for s in fb[:10]:
            print(f"  {s['file']} → {s['id']}（{s['slot']}）")
        print("  常见于改宏、注释、include：无法定位到具体函数，只按文件归属处理。")

    if empty:
        print("\n■ 未命中（库里没有对应符号）")
        for f in empty[:10]:
            print(f"  {_norm(f)}")
        print("  这些文件可能尚未抽取，考虑先跑 strata-run extract")

    seen: set[str] = set()
    seeds: list[dict] = []
    for s in matched + fb:
        if s["id"] in seen:
            continue
        seen.add(s["id"])
        seeds.append(s)

    if not seeds:
        print("\n结论：改动没有命中任何已知符号，无法给出影响面。")
        print("建议：先跑 strata-run extract <repo>，再跑 strata-run compile")
        return 0

    agg: dict[tuple[str, str], dict] = {}
    for s in seeds:
        res = analyze.impact(conn, s["id"], depth)
        for bucket, items in (res.get("buckets") or {}).items():
            for it in items:
                k = (it.get("slot", ""), it["id"])
                if k not in agg or it["depth"] < agg[k]["depth"]:
                    agg[k] = {"title": it.get("title", ""), "confidence": bucket,
                              "depth": it["depth"], "via": it.get("via", "")}

    labels = [("certain", "确定影响"), ("likely", "很可能影响"), ("possible", "可能影响")]
    counts = {}
    for key, label in labels:
        items = [v | {"slot": k[0], "id": k[1]} for k, v in agg.items() if v["confidence"] == key]
        counts[key] = len(items)
        print(f"\n■ {label}（{len(items)}）")
        if not items:
            print("  （无）")
            continue
        by_slot: dict[str, list] = {}
        for it in items:
            by_slot.setdefault(it["slot"], []).append(it)
        for slot in ("verification", "mechanism", "intent", "implementation"):
            group = by_slot.get(slot)
            if not group:
                continue
            print(f"  <{slot}> {len(group)}")
            for it in group[:limit]:
                print(f"    {it['id']}  {it['title'][:44]}")
            if len(group) > limit:
                print(f"    … 其余 {len(group) - limit} 条")

    print("\n■ 结论")
    tests = [k for k, v in agg.items() if k[0] == "verification"]
    if tests:
        print(f"  必跑用例 {len(tests)} 个（上表「很可能影响」中的 verification 组即候选集）")
    else:
        print("  没有找到受影响的用例：要么该符号确实无测试覆盖，要么覆盖率/匹配还没接上。")
    if counts.get("certain", 0) == 0:
        print("  「确定影响」为空：当前边来自静态匹配。接入覆盖率报告后这一档才会有内容。")
    return 0


def main(argv: list[str]) -> int:
    # --home <路径> 可以出现在任意位置：/strata-init /path/to/repo --home /path/to/strata
    explicit = None
    if "--home" in argv:
        i = argv.index("--home")
        if i + 1 >= len(argv):
            print("--home 后面要跟工程根路径", file=sys.stderr)
            return 2
        explicit = argv[i + 1]
        del argv[i:i + 2]
    for i, a in enumerate(argv):
        if a.startswith("--home="):
            explicit = a.split("=", 1)[1]
            del argv[i]
            break

    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0

    # home 是配置命令，不依赖已解析出的工程根
    if argv[0] == "home":
        return cmd_home(argv[1:])

    root = find_root(explicit)
    if root is None:
        print(NOT_FOUND, file=sys.stderr)
        if explicit:
            print(f"（你指定的是 {explicit}，但那里没有 strata.py + core/）", file=sys.stderr)
        return 2

    cmd = argv[0]
    if cmd == "where":
        return cmd_where(root)
    if cmd == "next":
        return cmd_next(root)
    if cmd == "drafts":
        return cmd_drafts(root)
    if cmd == "impact-diff":
        return cmd_impact_diff(root, argv[1:])

    return subprocess.run([sys.executable, str(root / "strata.py"), *argv]).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
