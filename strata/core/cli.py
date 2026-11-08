"""Strata 命令行入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import analyze, base, compiler


def add_gap(conn, hole: str, question: str, context: str = "") -> str:
    """登记缺口：先落 jsonl，再尽力写库。

    远端服务端是只读打开的，写库必然失败——这不是错误，
    jsonl 已经是事实源，下一次 compile 会把它回放进 gap 表。
    """
    gid = base.append_gap(hole, question, context)
    if conn is not None:
        try:
            conn.execute("INSERT OR REPLACE INTO gap(id,hole,question,context,status,created_at) "
                         "VALUES(?,?,?,?,?,?)", (gid, hole, question, context, "open", base.now()))
            conn.commit()
        except Exception:
            pass          # 只读索引：留给 compile 回放
    return gid


def cmd_compile(a) -> int:
    rep = compiler.compile_cards(Path(a.cards), Path(a.db), verbose=True)
    return 0 if rep.ok else 1


def cmd_holes(a) -> int:
    conn = base.connect()
    print(analyze.render_holes(analyze.find_holes(conn, a.limit)))
    return 0


def cmd_stat(a) -> int:
    conn = base.connect()
    print(analyze.stats(conn))
    return 0


def cmd_impact(a) -> int:
    conn = base.connect()
    print(analyze.render_impact(analyze.impact(conn, a.symbol, a.depth)))
    return 0


def cmd_coverage(a) -> int:
    conn = base.connect()
    print(analyze.render_coverage(analyze.coverage(conn, a.node, a.depth)))
    return 0


def cmd_extract(a) -> int:
    repo = Path(a.repo).expanduser()
    if not repo.is_dir():
        print(f"路径不存在：{repo}")
        return 2
    repo = repo.resolve()

    # 防止把工程自身当代码仓：那样会抽出一堆无关卡片并覆盖掉现有知识库
    if repo == base.ROOT or (repo / "strata.py").is_file() and (repo / "core").is_dir():
        print("拒绝：这是 Strata 工程自身，不是被分析的代码仓。")
        print(f"请在被分析的仓库目录执行，或指定路径：python strata.py extract <仓库路径>")
        return 2

    exts = (".h", ".hpp", ".cc", ".cpp", ".cxx")
    n_src = sum(1 for p in repo.rglob("*") if p.suffix in exts and ".git" not in p.parts)
    if n_src == 0:
        print(f"在 {repo} 下没有找到 C/C++ 源文件，抽取会产出空库。")
        print("确认路径是否正确；若不是 C/C++ 项目，需要另写抽取器。")
        return 2

    out = Path(a.out)
    if out.is_dir():
        existing = len(list(out.rglob("*.md")))
        if existing:
            print(f"注意：{out} 已有 {existing} 张卡片。同 id 会被覆盖，不同 id 会保留。")
            print("      换一个仓库抽取时，请用 --out 指向新目录，避免两个仓的卡片混在一起。\n")

    sys.path.insert(0, str(base.ROOT))
    from extractors import cpp_static
    cpp_static.extract(repo, pack=a.pack, out_dir=out,
                       max_tests=a.max_tests, verbose=True)
    return 0


def cmd_serve(a) -> int:
    from . import mcp_server
    mcp_server.main(a.serve_args)
    return 0


def cmd_gap(a) -> int:
    conn = base.connect()
    if a.gap_cmd == "add":
        gid = add_gap(conn, a.hole, a.question, a.context or "")
        print(f"已登记缺口 {gid}")
        return 0
    rows = conn.execute("SELECT * FROM gap ORDER BY created_at DESC LIMIT 50").fetchall()
    if not rows:
        print("暂无缺口记录")
        return 0
    for r in rows:
        print(f"{r['id']}  [{r['hole']}]  {r['status']}  {r['question'][:60]}")
    return 0


def cmd_viz(a) -> int:
    from . import viz
    try:
        dest = viz.build_html(a.db, a.out)
    except FileNotFoundError as e:
        print(e)
        return 2
    size = dest.stat().st_size / 1024
    print(f"已生成：{dest}")
    print(f"单文件 {size:.0f} KB，数据内嵌，不联网、不依赖任何前端库，可以直接发给人。")
    print(f"也可以挂在服务端上：python strata.py serve --http --port 8760 之后访问 http://<主机>:8760/")
    if a.open:
        import webbrowser
        webbrowser.open(dest.resolve().as_uri())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="strata", description="把散落的文档、测试与代码沉积成可查询的分层知识库")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compile", help="卡片 -> 索引")
    c.add_argument("--cards", default=str(base.CARDS_DIR))
    c.add_argument("--db", default=str(base.DB_PATH))
    c.set_defaults(func=cmd_compile)

    h = sub.add_parser("holes", help="扫描六类空洞")
    h.add_argument("--limit", type=int, default=5)
    h.set_defaults(func=cmd_holes)

    s = sub.add_parser("stat", help="知识库概况")
    s.set_defaults(func=cmd_stat)

    i = sub.add_parser("impact", help="查影响面")
    i.add_argument("symbol")
    i.add_argument("--depth", type=int, default=4)
    i.set_defaults(func=cmd_impact)

    v = sub.add_parser("coverage", help="查覆盖范围")
    v.add_argument("node")
    v.add_argument("--depth", type=int, default=4)
    v.set_defaults(func=cmd_coverage)

    e = sub.add_parser("extract", help="从 C++ 仓库抽取卡片")
    e.add_argument("repo")
    e.add_argument("--pack", default="generic-cpp")
    e.add_argument("--out", default=str(base.CARDS_DIR))
    e.add_argument("--max-tests", type=int, default=3000)
    e.set_defaults(func=cmd_extract)

    # serve 的参数原样透传：--http / --host / --port / --token / --db
    sub.add_parser("serve", help="启动 MCP 服务（默认 stdio，加 --http 走远端）",
                   add_help=False).set_defaults(func=cmd_serve)

    z = sub.add_parser("viz", help="导出知识库全景图（单文件 HTML，可直接浏览全部节点）")
    z.add_argument("--out", default=None,
                   help="输出路径，默认 docs/graph.html")
    z.add_argument("--db", default=str(base.DB_PATH))
    z.add_argument("--open", action="store_true", help="生成后用浏览器打开")
    z.set_defaults(func=cmd_viz)

    g = sub.add_parser("gap", help="缺口登记")
    gs = g.add_subparsers(dest="gap_cmd", required=True)
    ga = gs.add_parser("add")
    ga.add_argument("question")
    ga.add_argument("--hole", default="manual")
    ga.add_argument("--context", default="")
    gs.add_parser("list")
    g.set_defaults(func=cmd_gap)

    return p


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # serve 的选项由它自己解析（它要透传给 MCP 服务端），这里先剥出来
    serve_args: list[str] = []
    if argv[:1] == ["serve"]:
        serve_args, argv = argv[1:], ["serve"]

    args = build_parser().parse_args(argv)
    args.serve_args = serve_args
    return args.func(args)
