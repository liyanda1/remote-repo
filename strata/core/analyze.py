"""分析层：空洞扫描、影响面、覆盖查询。

所有结论按置信度三档分组输出，不合并——这是让结论能被信任的前提。
"""

from __future__ import annotations

import sqlite3
from collections import defaultdict

from . import base

# 向上传播的边（验证 -> 机制 -> 意图）
UP_EDGES = ("exercises", "verified_by", "composed_of", "fulfills")
# 向下展开的边
DOWN_EDGES = ("composed_of", "verified_by", "exercises", "fulfills", "depends_on")

HOLES = [
    ("H1-orphan-intent", "high", "意图没有任何机制实现它"),
    ("H2-unverified-mechanism", "high", "机制没有对应的验证用例"),
    ("H3-unmapped-verification", "medium", "用例没有映射到任何代码"),
    ("H4-unsourced-edge", "critical", "边缺少证据来源"),
    ("H5-single-path", "low", "关键机制只有单一入口，脆弱"),
    ("H6-conflict", "high", "存在被打上争议标记的节点"),
]
HOLE_DESC = {h[0]: {"severity": h[1], "desc": h[2]} for h in HOLES}


def _rows(conn, sql, args=()):
    return [dict(r) for r in conn.execute(sql, args).fetchall()]


# ------------------------------------------------------------------ 空洞扫描
def find_holes(conn: sqlite3.Connection, limit: int = 5) -> list[dict]:
    out = []

    def add(hole, sql, args=(), note=""):
        rows = _rows(conn, sql, args)
        out.append({
            "hole": hole,
            "severity": HOLE_DESC[hole]["severity"],
            "desc": HOLE_DESC[hole]["desc"],
            "note": note,
            "count": len(rows),
            "sample": rows[:limit],
        })

    add("H1-orphan-intent", """
        SELECT n.id, n.title FROM node n
        WHERE n.slot='intent'
          AND NOT EXISTS (SELECT 1 FROM edge e WHERE e.src=n.id AND e.type='composed_of')
        ORDER BY n.id LIMIT 2000
    """)
    add("H2-unverified-mechanism", """
        SELECT n.id, n.title FROM node n
        WHERE n.slot='mechanism'
          AND NOT EXISTS (SELECT 1 FROM edge e WHERE e.src=n.id AND e.type='verified_by')
        ORDER BY n.id LIMIT 2000
    """)
    add("H3-unmapped-verification", """
        SELECT n.id, n.title FROM node n
        WHERE n.slot='verification'
          AND NOT EXISTS (SELECT 1 FROM edge e WHERE e.src=n.id AND e.type='exercises')
        ORDER BY n.id LIMIT 2000
    """)
    add("H4-unsourced-edge", """
        SELECT src || ' ->' || type || '-> ' || dst AS id, type AS title FROM edge
        WHERE source_ref IS NULL OR TRIM(source_ref)=''
        LIMIT 2000
    """)
    add("H5-single-path", """
        SELECT m.id, m.title FROM node m
        WHERE m.slot='mechanism'
          AND (SELECT COUNT(*) FROM edge e WHERE e.dst=m.id AND e.type='composed_of') = 1
          AND EXISTS (
            SELECT 1 FROM edge e2 WHERE e2.dst=m.id AND e2.type='composed_of' AND e2.weight < 0.5
          )
        LIMIT 2000
    """)
    add("H6-conflict", """
        SELECT id, title FROM node WHERE status='disputed' LIMIT 2000
    """)
    return out


def render_holes(holes: list[dict]) -> str:
    L = []
    total = sum(h["count"] for h in holes)
    L.append("=" * 62)
    L.append(f"空洞扫描  共 {total} 处")
    L.append("=" * 62)
    for h in holes:
        flag = "  " if h["count"] == 0 else "! "
        L.append(f"{flag}{h['hole']:<26} {h['severity']:<9} {h['count']:>6}   {h['desc']}")
        for s in h["sample"][:3]:
            L.append(f"      - {s.get('id','')}  {str(s.get('title',''))[:48]}")
        if h["count"] > 3:
            L.append(f"      ... 其余 {h['count'] - 3} 条")
    return "\n".join(L)


# ------------------------------------------------------------------ 符号解析
def resolve(conn: sqlite3.Connection, needle: str) -> list[dict]:
    """按精确度依次尝试：id -> 标题全等 -> 标题后缀 -> 模糊。命中即返回。"""
    steps = [
        ("SELECT * FROM node WHERE id=?", (needle,)),
        ("SELECT * FROM node WHERE title=?", (needle,)),
        ("SELECT * FROM node WHERE title LIKE ? ORDER BY LENGTH(title) LIMIT 8", (f"%::{needle}",)),
        ("SELECT * FROM node WHERE title LIKE ? OR id LIKE ? ORDER BY LENGTH(title) LIMIT 8",
         (f"%{needle}%", f"%{needle}%")),
    ]
    for sql, args in steps:
        rows = _rows(conn, sql, args)
        if rows:
            return rows
    return []


# ------------------------------------------------------------------ 影响面
def impact(conn: sqlite3.Connection, needle: str, depth: int = 4) -> dict:
    seeds = resolve(conn, needle)
    if not seeds:
        return {"seed": needle, "found": False, "groups": {}, "paths": []}

    start_ids = [s["id"] for s in seeds]
    placeholders = ",".join("?" * len(start_ids))
    # 置信度沿路径取最小值：经过一条 likely 的边，结论就只能是 likely。
    sql = f"""
    WITH RECURSIVE up(id, depth, conf, via) AS (
      SELECT n.id, 0,
             CASE n.confidence WHEN 'certain' THEN 3 WHEN 'likely' THEN 2 ELSE 1 END,
             n.id
      FROM node n WHERE n.id IN ({placeholders})
      UNION ALL
      SELECT e.src, up.depth + 1,
             CASE
               WHEN up.conf < (CASE e.confidence WHEN 'certain' THEN 3
                                                  WHEN 'likely' THEN 2 ELSE 1 END)
               THEN up.conf
               ELSE (CASE e.confidence WHEN 'certain' THEN 3
                                       WHEN 'likely' THEN 2 ELSE 1 END)
             END,
             up.via || ' <-' || e.type || '- ' || e.src
      FROM edge e JOIN up ON e.dst = up.id
      WHERE e.type IN ('exercises','verified_by','composed_of','fulfills')
        AND up.depth < ?
    )
    SELECT id, depth, conf, via FROM up
    """
    rows = _rows(conn, sql, (*start_ids, depth))

    best: dict[str, dict] = {}
    for r in rows:
        cur = best.get(r["id"])
        if cur is None or (r["conf"], -r["depth"]) > (cur["conf"], -cur["depth"]):
            best[r["id"]] = r

    ids = list(best)
    if not ids:
        return {"seed": needle, "found": True, "groups": {}, "paths": []}
    ph = ",".join("?" * len(ids))
    nodes = {r["id"]: r for r in _rows(conn, f"SELECT * FROM node WHERE id IN ({ph})", ids)}

    rank_name = {3: "certain", 2: "likely", 1: "possible"}
    groups: dict[str, list] = defaultdict(list)
    for nid, r in best.items():
        n = nodes.get(nid)
        if not n:
            continue
        groups[n["slot"]].append({
            "id": nid, "title": n["title"], "status": n["status"],
            "confidence": rank_name[r["conf"]],
            "depth": r["depth"], "via": r["via"],
        })

    for slot in groups:
        groups[slot].sort(key=lambda x: (x["depth"], x["id"]))

    buckets: dict[str, list] = {"certain": [], "likely": [], "possible": []}
    for slot, items in groups.items():
        for it in items:
            if it["depth"] == 0:
                continue
            buckets[it["confidence"]].append({**it, "slot": slot})

    return {
        "seed": needle,
        "found": True,
        "seeds": [{"id": s["id"], "title": s["title"], "slot": s["slot"]} for s in seeds],
        "groups": dict(groups),
        "buckets": buckets,
        "total": sum(len(v) for v in buckets.values()),
    }


def render_impact(res: dict) -> str:
    L = []
    if not res["found"]:
        L.append(f"未找到符号：{res['seed']}")
        L.append("可先用 strata.py stat 或 grep 卡片目录确认名字。")
        return "\n".join(L)
    L.append("=" * 62)
    L.append(f"影响面：{res['seed']}")
    L.append("=" * 62)
    for s in res["seeds"][:5]:
        L.append(f"起点  {s['id']}  [{s['slot']}]  {s['title']}")
    L.append("")

    labels = [("certain", "确定影响"), ("likely", "很可能影响"), ("possible", "可能影响")]
    slot_order = ["intent", "mechanism", "verification", "implementation"]
    sample_path = None
    for key, label in labels:
        items = res["buckets"].get(key) or []
        L.append(f"[{label}]  {len(items)} 条")
        by_slot: dict[str, list] = defaultdict(list)
        for it in items:
            by_slot[it["slot"]].append(it)
        for slot in slot_order:
            group = by_slot.get(slot) or []
            if not group:
                continue
            L.append(f"   <{slot}>  {len(group)}")
            for it in group[:8]:
                L.append(f"      {it['id']}  {it['title'][:44]}")
                if sample_path is None and it["depth"] > 0:
                    sample_path = it["via"]
            if len(group) > 8:
                L.append(f"      ... 其余 {len(group) - 8} 条")
        L.append("")

    if sample_path:
        L.append("一条传播路径（可直接复核）：")
        L.append("   " + " \n   ".join(sample_path.split(" <-")))
        L.append("")
    if res["total"] == 0:
        L.append("（该符号没有任何上游关联，是一个孤岛节点）")
    return "\n".join(L)


# ------------------------------------------------------------------ 覆盖查询
def coverage(conn: sqlite3.Connection, needle: str, depth: int = 4) -> dict:
    seeds = resolve(conn, needle)
    if not seeds:
        return {"seed": needle, "found": False}
    ids = [s["id"] for s in seeds]
    ph = ",".join("?" * len(ids))
    sql = f"""
    WITH RECURSIVE down(id, depth) AS (
      SELECT id, 0 FROM node WHERE id IN ({ph})
      UNION
      SELECT e.dst, down.depth + 1
      FROM edge e JOIN down ON e.src = down.id
      WHERE e.type IN ('composed_of','verified_by','exercises')
        AND down.depth < ?
    )
    SELECT id, MIN(depth) AS depth FROM down GROUP BY id
    """
    rows = _rows(conn, sql, (*ids, depth))
    ids2 = [r["id"] for r in rows]
    ph2 = ",".join("?" * len(ids2))
    nodes = {r["id"]: r for r in _rows(conn, f"SELECT * FROM node WHERE id IN ({ph2})", ids2)}
    groups: dict[str, list] = defaultdict(list)
    for r in rows:
        n = nodes.get(r["id"])
        if n:
            groups[n["slot"]].append({"id": r["id"], "title": n["title"],
                                      "depth": r["depth"], "confidence": n["confidence"]})
    for s in groups:
        groups[s].sort(key=lambda x: (x["depth"], x["id"]))
    return {"seed": needle, "found": True, "groups": dict(groups),
            "total": sum(len(v) for v in groups.values())}


def render_coverage(res: dict) -> str:
    L = []
    if not res["found"]:
        L.append(f"未找到节点：{res['seed']}")
        return "\n".join(L)
    L.append("=" * 62)
    L.append(f"覆盖范围：{res['seed']}   共 {res['total']} 个节点")
    L.append("=" * 62)
    order = ["intent", "mechanism", "verification", "implementation"]
    for slot in order:
        items = res["groups"].get(slot) or []
        if not items:
            continue
        L.append(f"<{slot}>  {len(items)}")
        for it in items[:10]:
            L.append(f"   {'  ' * it['depth']}{it['id']}  {it['title'][:44]}")
        if len(items) > 10:
            L.append(f"   ... 其余 {len(items) - 10} 条")
        L.append("")
    return "\n".join(L)


# ------------------------------------------------------------------ 统计
def stats(conn: sqlite3.Connection) -> str:
    L = ["=" * 62, "知识库概况", "=" * 62]
    for r in conn.execute("SELECT slot, COUNT(*) c FROM node GROUP BY slot ORDER BY c DESC"):
        L.append(f"  {r['slot']:<16} {r['c']:>8}")
    L.append("")
    for r in conn.execute("SELECT type, COUNT(*) c FROM edge GROUP BY type ORDER BY c DESC"):
        L.append(f"  {r['type']:<16} {r['c']:>8}")
    L.append("")
    for r in conn.execute("SELECT confidence, COUNT(*) c FROM node GROUP BY confidence ORDER BY c DESC"):
        L.append(f"  {r['confidence']:<16} {r['c']:>8}")
    L.append("")
    for r in conn.execute("SELECT status, COUNT(*) c FROM node GROUP BY status ORDER BY c DESC"):
        L.append(f"  status {r['status']:<9} {r['c']:>8}")
    return "\n".join(L)


# ------------------------------------------------------------------ 证据链
def explain(conn: sqlite3.Connection, src: str, dst: str, etype: str) -> dict | None:
    r = conn.execute("SELECT * FROM edge WHERE src=? AND dst=? AND type=?",
                     (src, dst, etype)).fetchone()
    if not r:
        return None
    return dict(r)
