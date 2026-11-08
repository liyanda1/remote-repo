"""C++ 静态抽取器：源码 -> 卡片。

设计约束（很重要）：
  不依赖编译数据库、不依赖编译器、不跑测试。
  只用正则做语法级扫描，产出的边一律 confidence=likely，绝不标 certain。
  真实工程里，覆盖率与 ELF 那两条硬边应由 core 的对应抽取器补上。

四层产出：
  mechanism      = 一个公共头文件一个模块
  implementation = class / struct / 函数声明 / 类外定义
  verification   = gtest 的 TEST / TEST_F / TEST_P
  intent         = 文档二级标题，草稿状态，标题里出现模块名才自动连边

边方向严格遵守 core/schema.yaml：
  mechanism  -verified_by->  verification
  verification -exercises->  implementation
  intent     -composed_of->  mechanism
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml

from core import base

SKIP_DIRS = {".git", "build", "_build", "third_party", "vendor",
             "node_modules", ".github", "support"}

RE_CLASS = re.compile(r"^[ \t]*(?:template\s*<[^;{}]*>\s*)?(?:class|struct)\s+(\w+)\s*(?:[:{]|$)", re.M)
RE_FUNC = re.compile(
    r"^[ \t]*(?:template\s*<[^;{}]*>\s*)?"
    r"(?:inline\s+|constexpr\s+|static\s+|virtual\s+|explicit\s+|FMT_[A-Z_]+\s+)*"
    r"[\w:<>,~&*\s\[\]]*?"
    r"\b([A-Za-z_~]\w*)\s*\([^;{}]*\)\s*"
    r"(?:const\s*)?(?:noexcept\s*)?(?:->\s*[\w:<>,&\s]+)?\s*[;{]",
    re.M,
)
RE_DEF = re.compile(r"^[ \t]*(?:template<[^>]*>\s*)?[\w:<>,~&*\s]+?\b(\w+)::(~?\w+)\s*\(", re.M)
RE_TEST = re.compile(r"^[ \t]*TEST(?:_F|_P)?\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*\{?", re.M)
RE_INCLUDE = re.compile(r'^[ \t]*#\s*include\s*[<"]([^">]+)[">]', re.M)
# 不匹配 obj.method( 或 ptr->method(，只保留看起来像自由函数或 fqn::func( 的调用
RE_CALL = re.compile(r"(?<![.\w>])([A-Za-z_]\w{2,})\s*\(")
RE_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
# 行首到函数名之间若出现这些特征，说明这行是语句而不是定义
RE_STMT_HEAD = re.compile(r"^(?:return|throw|co_return)\b")
RE_STMT_TAIL = re.compile(r"(?:=|,)\s*$")
RE_H2U = re.compile(r"^##\s+(.+?)\s*$", re.M)

KEYWORDS = {
    "if", "for", "while", "switch", "return", "sizeof", "decltype", "alignof",
    "static_cast", "dynamic_cast", "const_cast", "reinterpret_cast", "new", "delete",
    "throw", "catch", "case", "do", "else", "defined", "assert", "using", "namespace",
    "TEST", "TEST_F", "TEST_P", "EXPECT_EQ", "EXPECT_TRUE", "EXPECT_FALSE",
    "ASSERT_EQ", "ASSERT_TRUE", "ASSERT_FALSE", "EXPECT_THROW", "ASSERT_THROW",
    "EXPECT_STREQ", "EXPECT_NE", "ASSERT_NE", "EXPECT_LT", "EXPECT_GT",
    "EXPECT_CALL", "ON_CALL", "MOCK_METHOD", "INSTANTIATE_TEST_SUITE_P",
}
SYMBOL_MIN = 4

# 常见容器/系统调用名，命中也不算覆盖，避免噪声边
STOP_CALLS = {
    "size", "data", "move", "begin", "end", "empty", "clear", "close", "open",
    "write", "read", "push", "pop", "back", "front", "insert", "erase", "find",
    "count", "substr", "append", "resize", "reserve", "swap", "length",
    "compare", "assign", "fill", "copy", "pipe", "print", "printf", "malloc",
    "free", "memcpy", "memset", "strlen", "strcmp", "abort", "exit",
}


def _slug(s: str) -> str:
    # 统一小写：Windows / macOS 文件系统大小写不敏感，Time 与 time 会撞成同一个文件
    return re.sub(r"[^A-Za-z0-9_.]+", "_", s).strip("_").lower() or "x"


class IdGen:
    """保证 id 唯一：slug 冲突时追加序号。"""

    def __init__(self):
        self.used: set[str] = set()

    def make(self, prefix: str, name: str) -> str:
        s = prefix + _slug(name)
        if s not in self.used:
            self.used.add(s)
            return s
        i = 2
        while f"{s}_{i}" in self.used:
            i += 1
        s = f"{s}_{i}"
        self.used.add(s)
        return s


def _iter_files(root: Path, suffixes: tuple[str, ...]):
    if not root.is_dir():
        return
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def _match_brace(text: str, start: int, limit: int = 20000) -> str:
    """从 start 起找第一个 { 并配平，返回函数体文本。"""
    i = text.find("{", start)
    if i < 0:
        return ""
    depth, j = 0, i
    end = min(len(text), i + limit)
    while j < end:
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1
    return text[i:end]


def _brace_end(text: str, start: int, limit: int = 20000) -> int:
    """返回从 start 起第一个 { 的配对 } 的位置；找不到返回 -1。

    用于给符号记录结束行，影响面查询才能按行范围定位到具体符号，
    而不是「改了这个文件就算动了里面所有符号」。
    """
    i = text.find("{", start)
    if i < 0:
        return -1
    depth, j = 0, i
    end = min(len(text), i + limit)
    while j < end:
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def _write_card(out_dir: Path, slot: str, fm: dict, body: str) -> None:
    d = out_dir / slot
    d.mkdir(parents=True, exist_ok=True)
    text = ("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False,
                                     default_flow_style=False)
            + "---\n\n" + body.strip() + "\n")
    (d / f"{fm['id']}.md").write_text(text, encoding="utf-8")


def extract(repo: Path, pack: str = "generic-cpp", out_dir: Path | None = None,
            max_tests: int = 3000, verbose: bool = True) -> dict:
    repo = Path(repo).resolve()
    out_dir = Path(out_dir or base.CARDS_DIR)
    ids = IdGen()
    stat = {"modules": 0, "symbols": 0, "tests": 0, "intents": 0,
            "edges_verified_by": 0, "edges_exercises": 0, "edges_composed_of": 0}

    # ------------------------------------------------ 1. 模块
    inc = repo / "include"
    header_root = inc if inc.is_dir() else repo
    modules: dict[str, dict] = {}
    for h in sorted(_iter_files(header_root, (".h", ".hpp"))):
        stem = h.stem
        if stem in modules:
            continue
        rel = h.relative_to(repo).as_posix()
        modules[stem] = {"id": ids.make("cpp.mod.", stem), "header": rel}

    # ------------------------------------------------ 2. 符号
    # 先按 (文件, 名字) 全量收集。同名函数常分布在多个头文件（format_to 在
    # fmt 里就有 8 处），若按名字去重，图里只剩一个，影响面会长期指错实现。
    raw: list[dict] = []
    files = list(_iter_files(header_root, (".h", ".hpp"))) + \
        list(_iter_files(repo / "src", (".cc", ".cpp")))
    for f in files:
        rel = f.relative_to(repo).as_posix()
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        def _add(name: str, kind: str, pos: int, _t: str = text, _r: str = rel) -> None:
            # 行首到名字之间必须是一段「类型」，否则多半是语句里的调用：
            #   format_to(out, fmt);        ← 前缀为空
            #   return format_to(out, f);   ← 前缀以 return 结尾
            #   auto x = format_to(...);    ← 前缀以 = 结尾
            # 这些不是定义，混进 locations 会让行级定位误判。
            ls = _t.rfind("\n", 0, pos) + 1
            prefix = _t[ls:pos].strip()
            if kind in ("function", "method"):
                if not prefix or RE_STMT_HEAD.match(prefix) or RE_STMT_TAIL.search(prefix):
                    return
            ln = _t[:pos].count("\n") + 1
            be = _brace_end(_t, pos)
            raw.append({"name": name, "kind": kind, "file": _r, "line": ln,
                        "line_end": _t[:be].count("\n") + 1 if be > 0 else ln})

        for m in RE_CLASS.finditer(text):
            name = m.group(1)
            if name in KEYWORDS or len(name) < SYMBOL_MIN:
                continue
            _add(name, "class", m.start(1))
        for m in RE_FUNC.finditer(text):
            name = m.group(1)
            if name in KEYWORDS or len(name) < SYMBOL_MIN or name.startswith("FMT_"):
                continue
            _add(name, "function", m.start(1))
        for m in RE_DEF.finditer(text):
            cls, meth = m.group(1), m.group(2).lstrip("~")
            if meth in KEYWORDS or len(meth) < SYMBOL_MIN:
                continue
            _add(f"{cls}::{meth}", "method", m.start(2))

    # 同名符号合并为一个节点，但保留全部出现位置：
    # - 声明在 .h、定义在 .cc 是同一个符号，拆成两个会让影响面断链；
    # - 跨文件的同名重载又必须能在多个位置上做行级定位。
    # 所以节点按名字唯一，位置存成列表。
    merged: dict[str, dict] = {}
    for s in raw:
        loc = {"file": s["file"], "line": s["line"],
               "line_end": s["line_end"], "kind": s["kind"]}
        cur = merged.get(s["name"])
        if cur is None:
            merged[s["name"]] = {**s, "locations": [loc]}
        else:
            cur["locations"].append(loc)
            if (s["file"], s["line"]) < (cur["file"], cur["line"]):
                cur.update({"file": s["file"], "line": s["line"],
                            "line_end": s["line_end"], "kind": s["kind"]})

    symbols = list(merged.values())
    used: set[str] = set()
    for s in symbols:
        cid = ids.make("cpp.sym.", s["name"])
        if cid in used:  # 极少见：不同名字被 slug 成同一个 id
            cid = ids.make("cpp.sym.", f"{Path(s['file']).stem}.{s['name']}")
        used.add(cid)
        s["id"] = cid
    by_name = merged

    # ------------------------------------------------ 3. 测试用例
    test_files = [p for p in _iter_files(repo, (".cc", ".cpp"))
                  if "test" in p.relative_to(repo).as_posix().lower()]
    tests: list[dict] = []
    for f in test_files:
        rel = f.relative_to(repo).as_posix()
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        incs = RE_INCLUDE.findall(text)
        for m in RE_TEST.finditer(text):
            if len(tests) >= max_tests:
                break
            body = _match_brace(text, m.start())
            tests.append({
                "suite": m.group(1), "case": m.group(2), "file": rel,
                "line": text[:m.start()].count("\n") + 1,
                "includes": incs, "body": body,
            })

    sym_names = set(by_name)
    module_of_file = {}
    for stem in modules:
        module_of_file[stem] = modules[stem]["id"]
    module_to_tests: dict[str, list[str]] = {m: [] for m in modules}
    for t in tests:
        t["id"] = ids.make("cpp.tst.", f"{t['suite']}.{t['case']}")
        t["symbols"] = sorted({c for c in RE_CALL.findall(t["body"])
                               if c in sym_names and c not in STOP_CALLS})[:40]
        # 模块归属优先用「被测符号所在的文件」，比 include 精确得多
        mods = set()
        for sn in t["symbols"]:
            stem = Path(by_name[sn]["file"]).stem
            if stem in module_of_file:
                mods.add(stem)
        if not mods:  # 兜底：没有可匹配符号时才退回 include 关系
            mods = {Path(i).stem for i in t["includes"] if Path(i).stem in modules}
        t["modules"] = sorted(mods)
        for mod in t["modules"]:
            module_to_tests[mod].append(t["id"])

    # ------------------------------------------------ 4. 能力（文档标题）
    doc_dirs = [repo / "doc", repo / "docs"]
    doc_files: list[Path] = []
    for d in doc_dirs:
        doc_files += list(_iter_files(d, (".md",)))
    for nm in ("README.md", "readme.md"):
        p = repo / nm
        if p.exists():
            doc_files.append(p)

    intents: list[dict] = []
    seen_head: set[str] = set()
    for f in doc_files:
        rel = f.relative_to(repo).as_posix()
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in RE_H2.finditer(text):
            head = re.sub(r"[`*]", "", m.group(1)).strip()
            key = head.lower()
            if len(head) < 4 or key in seen_head:
                continue
            if key in {"license", "contributing", "table of contents", "api reference"}:
                continue
            seen_head.add(key)
            intents.append({"heading": head, "file": rel,
                            "line": text[:m.start()].count("\n") + 1})

    # ------------------------------------------------ 5. 落盘
    for stem, mo in modules.items():
        titles = module_to_tests.get(stem, [])
        _write_card(out_dir, "mechanism", {
            "id": mo["id"], "slot": "mechanism", "domain": pack,
            "title": f"{stem} 模块",
            "status": "confirmed", "confidence": "certain",
            "source": "extractor", "source_ref": f"{mo['header']}:1",
            "module": stem, "header": mo["header"],
            "links": [{"to": t, "type": "verified_by", "weight": 0.5} for t in titles],
            "evidence": [{"ref": f"{mo['header']}:1", "note": "公共头文件"}],
        }, f"## 模块\n`{stem}`，头文件 `{mo['header']}`。\n\n"
           f"由 cpp_static 按头文件粒度抽取，验证用例 {len(titles)} 个。")
        stat["modules"] += 1
        stat["edges_verified_by"] += len(titles)

    for s in symbols:
        name = s["name"]
        _write_card(out_dir, "implementation", {
            "id": s["id"], "slot": "implementation", "domain": pack,
            "title": name,
            "status": "confirmed", "confidence": "certain",
            "source": "extractor", "source_ref": f"{s['file']}:{s['line']}",
            "name": name, "kind": s["kind"], "file": s["file"], "line": s["line"],
            "line_end": s.get("line_end", s["line"]),
            "locations": s.get("locations", []),
            "links": [], "evidence": [{"ref": f"{s['file']}:{s['line']}", "note": s["kind"]}],
        }, f"## 符号\n`{name}`（{s['kind']}），位于 `{s['file']}`。\n\n"
           f"语法级抽取，未做类型推导。")
        stat["symbols"] += 1

    for t in tests:
        links = [{"to": by_name[h]["id"], "type": "exercises", "weight": 1.0}
                 for h in t["symbols"]]
        _write_card(out_dir, "verification", {
            "id": t["id"], "slot": "verification", "domain": pack,
            "title": f"{t['suite']}.{t['case']}",
            "status": "confirmed", "confidence": "likely",
            "source": "extractor", "source_ref": f"{t['file']}:{t['line']}",
            "suite": t["suite"], "case": t["case"],
            "file": t["file"], "line": t["line"],
            "links": links,
            "evidence": [{"ref": f"{t['file']}:{t['line']}", "note": "gtest 用例"}],
        }, f"## 用例\n`{t['suite']}.{t['case']}`\n\n"
           f"文件 `{t['file']}:{t['line']}`，覆盖符号 {len(links)} 个。\n\n"
           f"边来自静态调用匹配，置信度 likely。")
        stat["tests"] += 1
        stat["edges_exercises"] += len(links)

    for it in intents:
        hid = ids.make("cpp.cap.", it["heading"])
        low = it["heading"].lower()
        links = [{"to": modules[s]["id"], "type": "composed_of", "weight": 1.0}
                 for s in modules if s.lower() in low]
        stat["edges_composed_of"] += len(links)
        _write_card(out_dir, "intent", {
            "id": hid, "slot": "intent", "domain": pack,
            "title": it["heading"],
            "status": "proposed" if links else "draft",
            "confidence": "possible",
            "source": "extractor", "source_ref": f"{it['file']}:{it['line']}",
            "heading": it["heading"], "links": links,
            "evidence": [{"ref": f"{it['file']}:{it['line']}", "note": "文档二级标题"}],
        }, f"## 能力\n{it['heading']}\n\n从 `{it['file']}` 抽取的草稿，"
           f"需人工确认后再升级 status。\n\n关联模块 {len(links)} 个。")
        stat["intents"] += 1

    if verbose:
        print(f"抽取完成  模块 {stat['modules']}  符号 {stat['symbols']}  "
              f"用例 {stat['tests']}  能力 {stat['intents']}")
        print(f"边         verified_by {stat['edges_verified_by']}  "
              f"exercises {stat['edges_exercises']}  composed_of {stat['edges_composed_of']}")
    return stat
