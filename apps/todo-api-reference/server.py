"""SPEC-compatible Todo HTTP API (Python reference for oracle verification).

F1 SPEC locks Rust for production plans; this reference exists so
`fixtures/todo-api/oracle` can be executed in environments without rustc.
Formal ABP execute-to-score of arm plans still targets Rust when cargo is available.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DB_PATH = os.environ.get("DATABASE_URL", "sqlite:todos.db")
if DB_PATH.startswith("sqlite:"):
    DB_PATH = DB_PATH[len("sqlite:") :]
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8080"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def migrate() -> None:
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              completed INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )


def row_to_todo(r: sqlite3.Row) -> dict:
    return {
        "id": r["id"],
        "title": r["title"],
        "completed": bool(r["completed"]),
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
    }


def error(code: str, message: str, status: int) -> tuple[int, dict]:
    return status, {"error": {"code": code, "message": message}}


class Handler(BaseHTTPRequestHandler):
    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _send(self, status: int, body: dict | list | None = None) -> None:
        data = b"" if body is None else json.dumps(body).encode("utf-8")
        self.send_response(status)
        if body is not None:
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if data:
            self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self._send(200, {"status": "ok"})
        if parsed.path == "/todos":
            qs = parse_qs(parsed.query)
            completed = qs.get("completed", [None])[0]
            with db() as conn:
                if completed is None:
                    rows = conn.execute("SELECT * FROM todos").fetchall()
                elif completed in ("true", "false"):
                    flag = 1 if completed == "true" else 0
                    rows = conn.execute("SELECT * FROM todos WHERE completed = ?", (flag,)).fetchall()
                else:
                    st, body = error("validation_error", "invalid completed query", 400)
                    return self._send(st, body)
            return self._send(200, [row_to_todo(r) for r in rows])
        m = re.fullmatch(r"/todos/([^/]+)", parsed.path)
        if m:
            with db() as conn:
                row = conn.execute("SELECT * FROM todos WHERE id = ?", (m.group(1),)).fetchone()
            if not row:
                st, body = error("not_found", "todo not found", 404)
                return self._send(st, body)
            return self._send(200, row_to_todo(row))
        st, body = error("not_found", "route not found", 404)
        self._send(st, body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/todos":
            st, body = error("not_found", "route not found", 404)
            return self._send(st, body)
        payload = self._read_json()
        title = (payload.get("title") or "").strip()
        if not title or len(title) > 200:
            st, body = error("validation_error", "title must be 1..=200 chars", 400)
            return self._send(st, body)
        completed = bool(payload.get("completed", False))
        now = utc_now()
        tid = str(uuid.uuid4())
        with db() as conn:
            conn.execute(
                "INSERT INTO todos (id, title, completed, created_at, updated_at) VALUES (?,?,?,?,?)",
                (tid, title, int(completed), now, now),
            )
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
        self._send(201, row_to_todo(row))

    def do_PATCH(self) -> None:  # noqa: N802
        m = re.fullmatch(r"/todos/([^/]+)", self.path)
        if not m:
            st, body = error("not_found", "route not found", 404)
            return self._send(st, body)
        payload = self._read_json()
        if not payload:
            st, body = error("validation_error", "empty patch body", 400)
            return self._send(st, body)
        with db() as conn:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (m.group(1),)).fetchone()
            if not row:
                st, body = error("not_found", "todo not found", 404)
                return self._send(st, body)
            title = row["title"]
            completed = row["completed"]
            if "title" in payload:
                title = (payload.get("title") or "").strip()
                if not title or len(title) > 200:
                    st, body = error("validation_error", "title must be 1..=200 chars", 400)
                    return self._send(st, body)
            if "completed" in payload:
                completed = int(bool(payload["completed"]))
            now = utc_now()
            conn.execute(
                "UPDATE todos SET title=?, completed=?, updated_at=? WHERE id=?",
                (title, completed, now, m.group(1)),
            )
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (m.group(1),)).fetchone()
        self._send(200, row_to_todo(row))

    def do_DELETE(self) -> None:  # noqa: N802
        m = re.fullmatch(r"/todos/([^/]+)", self.path)
        if not m:
            st, body = error("not_found", "route not found", 404)
            return self._send(st, body)
        with db() as conn:
            cur = conn.execute("DELETE FROM todos WHERE id = ?", (m.group(1),))
            if cur.rowcount == 0:
                st, body = error("not_found", "todo not found", 404)
                return self._send(st, body)
        self._send(204, None)


def main() -> None:
    migrate()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"listening on http://{HOST}:{PORT} db={DB_PATH}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
