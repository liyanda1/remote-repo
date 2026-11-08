"""图视图：把索引导出成一份自包含的 HTML。

为什么不做成「前端直连 SQLite」：浏览器没有 SQLite。
为什么不做成「起服务再查」：单文件才能发给别人、才能挂 Git、才能离线看。
所以这里把数据内嵌进 HTML，页面本身零依赖、零网络请求。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import base

# 前端只认这四种颜色，顺序不能变（页面里按索引取色）
SLOT_ORDER = list(base.SLOTS)


def _props(raw: str | None) -> dict:
    if not raw:
        return {}
    try:
        v = json.loads(raw)
        return v if isinstance(v, dict) else {}
    except json.JSONDecodeError:
        return {}


def _file_of(node: sqlite3.Row, props: dict) -> str:
    """取节点所属文件。implementation 在 props.file，其余在 source_ref 里。

    这个字段是布局的关键：代码列按文件聚簇，开发者才能按自己熟悉的方式找到符号。
    """
    f = props.get("file")
    if f:
        return str(f)
    ref = node["source_ref"] or ""
    # source_ref 形如 include/fmt/format.h:4686，去掉行号
    if ":" in ref:
        head = ref.rsplit(":", 1)[0]
        if "." in head or "/" in head:
            return head
    return ref


def export_data(conn: sqlite3.Connection, *, body: bool = True) -> dict:
    """导出前端要的全部数据。顶点带编号，边用编号引用，省一半体积。"""
    rows = conn.execute(
        "SELECT id, slot, domain, title, status, confidence, source, source_ref, "
        "       body, card_path, props FROM node ORDER BY slot, id"
    ).fetchall()

    idx: dict[str, int] = {}
    nodes: list[dict] = []
    for r in rows:
        p = _props(r["props"])
        locs = p.get("locations") or []
        idx[r["id"]] = len(nodes)
        n = {
            "id": r["id"],
            "slot": r["slot"],
            "title": r["title"],
            "status": r["status"],
            "conf": r["confidence"],
            "src": r["source"],
            "ref": r["source_ref"] or "",
            "file": _file_of(r, p),
            "kind": p.get("kind", ""),
            "line": p.get("line", 0),
            "lineEnd": p.get("line_end", 0),
            "nLoc": len(locs) if locs else (1 if p.get("line") else 0),
        }
        if body:
            n["body"] = r["body"] or ""
        nodes.append(n)

    edges: list[dict] = []
    for e in conn.execute(
        "SELECT src, dst, type, weight, confidence, source_ref, evidence FROM edge"
    ).fetchall():
        a, b = idx.get(e["src"]), idx.get(e["dst"])
        if a is None or b is None:
            continue
        ev = ""
        try:
            items = json.loads(e["evidence"] or "[]")
            if items:
                ev = str(items[0].get("note") or items[0].get("ref") or "")
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
        edges.append({"a": a, "b": b, "t": e["type"], "w": e["weight"],
                      "c": e["confidence"], "ref": e["source_ref"] or "", "ev": ev})

    gaps = [dict(r) for r in conn.execute(
        "SELECT id, hole, question, context, status FROM gap ORDER BY id"
    ).fetchall()]

    meta_row = conn.execute("SELECT v FROM meta WHERE k='compiled_at'").fetchone()

    return {
        "meta": {
            "compiled_at": meta_row["v"] if meta_row else "",
            "nodes": len(nodes),
            "edges": len(edges),
            "gaps": len(gaps),
            "slots": SLOT_ORDER,
            "edge_types": list(base.EDGE_TYPES),
        },
        "nodes": nodes,
        "edges": edges,
        "gaps": gaps,
    }


def data_size(data: dict) -> int:
    return len(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def render_html(data: dict, template: Path | None = None) -> str:
    """把数据灌进模板。用 replace 而不是 format：模板里有大量 JS 花括号。"""
    tpl_path = template or (base.CORE_DIR / "viz_template.html")
    tpl = tpl_path.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> 出现在数据里会提前闭合脚本块，必须转义
    payload = payload.replace("</", "<\\/")
    if "__STRATA_DATA__" not in tpl:
        raise RuntimeError(f"模板缺少占位符 __STRATA_DATA__：{tpl_path}")
    return tpl.replace("__STRATA_DATA__", payload)


def build_html(db_path: Path | str | None = None, out: Path | str | None = None) -> Path:
    conn = base.connect_readonly(db_path or base.DB_PATH)
    try:
        data = export_data(conn)
    finally:
        conn.close()
    html = render_html(data)
    dest = Path(out) if out else (base.ROOT / "docs" / "graph.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return dest
