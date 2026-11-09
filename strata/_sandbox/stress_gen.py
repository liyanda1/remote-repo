"""合成一份用户内网规模的数据（5 场景 / 1600 功能点 / 13000 用例 / 7800 代码），
不走 SQLite，直接构造导出结构渲染页面，专门压测布局与虚拟化渲染。"""
import json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import viz

random.seed(42)
N, E = [], []

def node(nid, slot, title, **kw):
    N.append({"id": nid, "slot": slot, "title": title, "status": "confirmed",
              "conf": "certain", "src": "extractor", "ref": "", "file": kw.get("file", ""),
              "kind": kw.get("kind", ""), "line": kw.get("line", 0), "lineEnd": 0,
              "nLoc": 0, "body": ""})
    return len(N) - 1

def edge(a, b, t, c="certain"):
    E.append({"a": a, "b": b, "t": t, "w": 1.0, "c": c, "ref": "", "ev": ""})

# 5 个场景
intents = [node(f"scn.{i}", "intent", f"场景 {i:02d}·业务能力描述文字") for i in range(5)]
# 1600 个功能点，每个挂一个场景
mechs = []
for m in range(1600):
    mi = m % 5
    mechs.append(node(f"mech.{m:04d}", "mechanism", f"功能点 {m:04d} 状态与事件处理",
                      file=f"module_{m%40:02d}"))
    edge(intents[mi], mechs[-1], "composed_of")
# 13000 个用例，每个挂一个功能点；80% 有 exercises 边
impls = []
files = [f"src/sub{i%12}/unit_{i:02d}.cc" for i in range(60)]
for f in files:
    impls.append(node(f"sym.{f}", "implementation", f.split("/")[-1][:-3] + "_func",
                      file=f, kind="function", line=random.randint(1, 2000)))
for v in range(13000):
    mi = mechs[v % 1600]
    vi = node(f"tst.{v:05d}", "verification", f"TEST(suite_{v%200:03d}, case_{v:05d})",
              file=f"test/suite_{v%200:03d}.cc", line=v)
    edge(mi, vi, "verified_by")
    if v % 5 < 4:  # 80% 覆盖
        edge(vi, impls[v % 60], "exercises", random.choice(["likely", "likely", "possible"]))

data = {
    "meta": {"compiled_at": "2026-11-09T23:00:00", "nodes": len(N), "edges": len(E),
             "gaps": 0, "slots": viz.SLOT_ORDER, "edge_types": list(E.__len__() * [0])},
    "nodes": N, "edges": E, "gaps": [],
}
data["meta"]["edge_types"] = sorted({e["t"] for e in E})
html = viz.render_html(data)
out = Path("_sandbox/stress.html")
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"节点 {len(N)}  边 {len(E)}  HTML {out}  {len(html)//1024} KB")
