"""MCP 服务（stdio 与 Streamable HTTP 双传输）。

设计原则：对外只暴露语义化分析工具，不暴露裸图查询。
每个返回值都带置信度分组，避免把「可能」说成「确定」。

两种传输对应两种部署：
- stdio：一人一机，OpenCode 直接拉起子进程，读本机 index.sqlite。
- http ：一台机器起服务，全组通过远端 MCP 连过来共用同一份库。
        服务端只读打开索引（mode=ro），并发访问靠 SQLite 自身的读锁，
        不需要额外加锁，也不可能被查询请求改坏数据。
"""

from __future__ import annotations

import json
import sys
import threading
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import analyze, base

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "strata"

# 全景图缓存：(索引 mtime, HTML)。库没变就不重算，变了下一次请求自动重建。
_VIZ_CACHE: dict = {}

TOOLS = [
    {
        "name": "impact_of_change",
        "description": "给定一个代码符号、文件或卡片 id，反向追溯受影响的测试用例、模块与能力。"
                       "结果按「确定/很可能/可能」三档分组，并给出传播路径。改代码前调用。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "符号名、符号 id 或卡片 id"},
                "depth": {"type": "integer", "default": 4, "description": "最大回溯跳数"},
            },
            "required": ["symbol"],
        },
    },
    {
        "name": "coverage_of_intent",
        "description": "给定一个能力/场景节点，正向展开它覆盖到的模块、用例与代码符号。",
        "inputSchema": {
            "type": "object",
            "properties": {"intent": {"type": "string"}, "depth": {"type": "integer", "default": 4}},
            "required": ["intent"],
        },
    },
    {
        "name": "find_holes",
        "description": "扫描知识库的六类结构空洞，返回待补清单。用于驱动人工或问答补全。",
        "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer", "default": 5}}},
    },
    {
        "name": "graph_stats",
        "description": "知识库规模概况：各槽位节点数、各类型边数、置信度分布。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "explain_edge",
        "description": "查询一条边的证据来源（文件行号、报告、对话 id），用于审计结论。",
        "inputSchema": {
            "type": "object",
            "properties": {"src": {"type": "string"}, "dst": {"type": "string"},
                           "type": {"type": "string"}},
            "required": ["src", "dst", "type"],
        },
    },
    {
        "name": "log_gap",
        "description": "登记一个未覆盖的问题。查不到答案时调用，把缺口落成待办，不要编造答案。",
        "inputSchema": {
            "type": "object",
            "properties": {"hole": {"type": "string"}, "question": {"type": "string"},
                           "context": {"type": "string"}},
            "required": ["question"],
        },
    },
]


INSTRUCTIONS = (
    "Strata 代码知识库。回答「改这段代码影响什么」「这个能力覆盖到哪些用例」"
    "「这个结论凭什么」这类问题前，先调用对应工具，不要凭印象作答。"
    "查询结果分三档：确定 / 很可能 / 可能。转述时必须保留档位，不许合并成一堆。"
    "查不到就调 log_gap 登记并把问题抛回给用户，不许编造文件名、行号或阈值。"
)


def _text(s: str, is_error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": s}], "isError": is_error}


def _dispatch(conn, name: str, args: dict) -> dict:
    if name == "impact_of_change":
        res = analyze.impact(conn, args["symbol"], int(args.get("depth", 4)))
        return _text(analyze.render_impact(res))
    if name == "coverage_of_intent":
        res = analyze.coverage(conn, args["intent"], int(args.get("depth", 4)))
        return _text(analyze.render_coverage(res))
    if name == "find_holes":
        return _text(analyze.render_holes(analyze.find_holes(conn, int(args.get("limit", 5)))))
    if name == "graph_stats":
        return _text(analyze.stats(conn))
    if name == "explain_edge":
        e = analyze.explain(conn, args["src"], args["dst"], args["type"])
        if not e:
            return _text("未找到该边", is_error=True)
        return _text(json.dumps(e, ensure_ascii=False, indent=2))
    if name == "log_gap":
        from . import cli
        gid = cli.add_gap(conn, args.get("hole", "manual"),
                          args["question"], args.get("context", ""))
        return _text(f"已登记缺口 {gid}")
    return _text(f"未知工具：{name}", is_error=True)


def handle(conn, req: dict) -> dict | None:
    method = req.get("method")
    rid = req.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": "0.2.0"},
            "instructions": INSTRUCTIONS,
        }}
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        try:
            return {"jsonrpc": "2.0", "id": rid,
                    "result": _dispatch(conn, params.get("name", ""), params.get("arguments") or {})}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": rid,
                    "result": _text(f"工具执行失败：{e}", is_error=True)}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if rid is None:
        return None
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


def _stdio_main(db_path) -> None:
    """本地模式：OpenCode 拉起子进程，走 stdin/stdout。
    索引可写，所以 log_gap 能立刻落库，不必等下一次编译。"""
    conn = base.connect(db_path)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(conn, req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


# ------------------------------------------------------------------ HTTP 传输
class _Sessions:
    """内存里的会话表。服务重启即失效，客户端会重新 initialize，无需持久化。"""

    def __init__(self) -> None:
        self._ids: set[str] = set()
        self._lock = threading.Lock()

    def new(self) -> str:
        sid = uuid.uuid4().hex
        with self._lock:
            self._ids.add(sid)
        return sid

    def has(self, sid: str) -> bool:
        with self._lock:
            return sid in self._ids

    def drop(self, sid: str) -> None:
        with self._lock:
            self._ids.discard(sid)


class _Handler(BaseHTTPRequestHandler):
    server_version = "strata-mcp/0.2"
    protocol_version = "HTTP/1.1"

    # 由 make_server 注入
    db_path = base.DB_PATH
    token: str | None = None
    sessions: _Sessions = _Sessions()
    _local = threading.local()

    # ---------------- 基础设施 ----------------
    def log_message(self, fmt: str, *args) -> None:      # 默认日志太吵，压成一行
        sys.stderr.write("[mcp] %s - %s\n" % (self.address_string(), fmt % args))

    def _conn(self):
        """每个请求一个只读连接，用完即关。

        ThreadingHTTPServer 是「一请求一线程」，线程局部连接既不会被复用，
        还会漏文件句柄，所以这里干脆按请求开。
        SQLite 打开一个只读库是微秒级操作，代价可以忽略；
        好处是重建索引后不用重启服务——下一个请求就能读到新数据。
        """
        return base.connect_readonly(self.db_path)

    def _send(self, code: int, body: bytes = b"", ctype: str = "application/json",
              extra: dict | None = None) -> None:
        self.send_response(code)
        if body:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _json(self, code: int, obj, extra: dict | None = None) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json", extra)

    def _authorized(self) -> bool:
        if not self.token:
            return True
        got = self.headers.get("Authorization", "")
        if got == f"Bearer {self.token}":
            return True
        # 浏览器直接打开页面时带不了自定义头，允许 ?token= 兜底。
        # 页面是自包含的（数据内嵌），所以鉴权只能在这一层做，必须做。
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        return q.get("token", [""])[0] == self.token

    # ---------------- 路由 ----------------
    def do_POST(self) -> None:            # noqa: N802
        if self.path.rstrip("/") not in ("/mcp", ""):
            self._json(404, {"error": "not found"})
            return
        if not self._authorized():
            self._json(401, {"error": "unauthorized"},
                       {"WWW-Authenticate": 'Bearer realm="strata"'})
            return

        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b""
            payload = json.loads(raw.decode("utf-8"))
        except Exception as e:
            self._json(400, {"jsonrpc": "2.0", "id": None,
                             "error": {"code": -32700, "message": f"parse error: {e}"}})
            return

        batch = isinstance(payload, list)
        reqs = payload if batch else [payload]

        # 会话校验：带了 id 就必须是认识的，否则让客户端重新 initialize
        sid = self.headers.get("Mcp-Session-Id")
        if sid and not self.sessions.has(sid):
            self._json(404, {"error": "session expired, please initialize again"})
            return

        conn = self._conn()
        out = []
        try:
            for req in reqs:
                resp = handle(conn, req) if isinstance(req, dict) else None
                if resp is not None:
                    out.append(resp)
                if isinstance(req, dict) and req.get("method") == "initialize":
                    sid = self.sessions.new()
        finally:
            conn.close()

        extra = {"Mcp-Session-Id": sid} if sid else None
        if not out:
            # 只有通知，没有响应体：规范要求 202
            self._send(202, b"", extra=extra)
            return
        self._json(200, out if batch else out[0], extra)

    def do_GET(self) -> None:             # noqa: N802
        route = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
        if route in ("/", "/viz", "/graph"):
            self._serve_viz()
            return
        if route != "/healthz":
            # 不提供服务端主动推送的流；规范允许 405
            self._send(405, b'{"error":"use POST /mcp"}', extra={"Allow": "POST, DELETE"})
            return
        try:
            c = self._conn()
            try:
                n = c.execute("SELECT COUNT(*) c FROM node").fetchone()["c"]
                e = c.execute("SELECT COUNT(*) c FROM edge").fetchone()["c"]
                row = c.execute("SELECT v FROM meta WHERE k='compiled_at'").fetchone()
            finally:
                c.close()
            self._json(200, {"ok": True, "nodes": n, "edges": e,
                             "compiled_at": row["v"] if row else None,
                             "db": str(self.db_path)})
        except Exception as e:
            self._json(503, {"ok": False, "error": str(e)})

    def _serve_viz(self) -> None:
        """全景图：现场从只读索引生成，重编之后刷新页面就是新图。

        结果按索引 mtime 缓存——1506 个节点现算约 100ms，
        全组同时刷会明显拖慢，而库没变时没必要重算。
        """
        global _VIZ_CACHE
        if not self._authorized():
            self._json(401, {"error": "unauthorized"},
                       {"WWW-Authenticate": 'Bearer realm="strata"'})
            return
        try:
            from . import viz
            mtime = Path(self.db_path).stat().st_mtime_ns
            if _VIZ_CACHE.get("mtime") != mtime:
                conn = base.connect_readonly(self.db_path)
                try:
                    html = viz.render_html(viz.export_data(conn))
                finally:
                    conn.close()
                _VIZ_CACHE = {"mtime": mtime, "html": html}
            body = _VIZ_CACHE["html"].encode("utf-8")
            self._send(200, body, "text/html; charset=utf-8",
                       {"Cache-Control": "no-store"})
        except Exception as e:
            self._json(500, {"error": f"生成全景图失败：{e}"})

    def do_DELETE(self) -> None:           # noqa: N802
        sid = self.headers.get("Mcp-Session-Id")
        if sid:
            self.sessions.drop(sid)
        self._send(200, b"{}", extra={"Mcp-Session-Id": sid or ""})


def _http_main(db_path, host: str, port: int, token: str | None) -> None:
    try:
        conn = base.connect_readonly(db_path)      # 启动即验证索引可读
        n = conn.execute("SELECT COUNT(*) c FROM node").fetchone()["c"]
        conn.close()
    except Exception as e:
        print(f"[mcp] 无法打开索引：{e}", file=sys.stderr)
        raise SystemExit(2)

    h = type("BoundHandler", (_Handler,), {"db_path": db_path, "token": token})
    srv = ThreadingHTTPServer((host, port), h)
    srv.daemon_threads = True
    print(f"[mcp] Strata MCP 服务已启动  http://{host}:{port}/mcp", file=sys.stderr)
    print(f"[mcp] 索引 {db_path}（{n} 节点，只读）", file=sys.stderr)
    print(f"[mcp] 鉴权 {'Bearer token' if token else '未开启（仅限可信网段）'}", file=sys.stderr)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[mcp] 已停止", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="strata serve", description="Strata MCP 服务端")
    ap.add_argument("--http", action="store_true", help="用 HTTP 传输（多人远端共用）")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1")
    ap.add_argument("--port", type=int, default=8760, help="监听端口，默认 8760")
    ap.add_argument("--token", default=None,
                    help="Bearer token；内网多人用时建议设置，或留空只靠网段隔离")
    ap.add_argument("--db", default=str(base.DB_PATH), help="索引路径")
    a, _ = ap.parse_known_args(argv or [])

    if a.http:
        _http_main(a.db, a.host, a.port, a.token)
    else:
        _stdio_main(a.db)
