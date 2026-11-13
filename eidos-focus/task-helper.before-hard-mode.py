"""Small compatibility API for approved legacy Eidos Focus builds.

The installed executable predates the task-toggle endpoint. This local-only
companion preserves the legacy progress.json schema and exits with the app.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import shutil
import tempfile
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STATE = Path.home() / ".eidos_learning_tracker" / "progress.json"
TASK_ID = re.compile(r"^[A-Za-z0-9_.-]{1,120}$")
ORIGIN = "http://127.0.0.1:8765"


def update_task(path: Path, task_id: str, done: bool) -> dict[str, object]:
    if not TASK_ID.fullmatch(task_id):
        raise ValueError("Некорректный идентификатор задания")
    raw = path.read_bytes() if path.exists() else b"{}"
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("progress.json должен содержать JSON-объект")
    completed = set(map(str, data.setdefault("completed", [])))
    if done:
        completed.add(task_id)
    else:
        completed.discard(task_id)
    data["completed"] = sorted(completed)
    records = data.setdefault("task_records", {})
    record = records.setdefault(task_id, {"attempts": []})
    stamp = datetime.now().isoformat(timespec="minutes")
    status = "solved" if done else "retry"
    record.update({"status": status, "updated_at": stamp})
    record.setdefault("attempts", []).append({"status": status, "at": stamp, "note": "Eidos Focus"})
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        first_backup = path.with_name("progress.before_eidos_focus.json")
        if not first_backup.exists():
            shutil.copy2(path, first_backup)
        shutil.copy2(path, path.with_name("progress.last-good.json"))
    encoded = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    fd, temp_name = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return {"ok": True, "task_id": task_id, "done": done}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        return

    def headers_common(self):
        self.send_header("Access-Control-Allow-Origin", ORIGIN)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")

    def send_json(self, value: object, status: int = 200):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.headers_common()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.headers_common()
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/task":
            return self.send_json({"error": "Not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            self.send_json(update_task(STATE, str(body.get("task_id", "")), bool(body.get("done"))))
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, 400)
        except Exception as exc:
            self.send_json({"error": f"Не удалось сохранить: {exc}"}, 500)


def watch_process(server: ThreadingHTTPServer, pid: int):
    synchronize = 0x00100000
    handle = ctypes.windll.kernel32.OpenProcess(synchronize, False, pid)
    if not handle:
        server.shutdown()
        return
    try:
        while ctypes.windll.kernel32.WaitForSingleObject(handle, 500) == 0x00000102:
            time.sleep(0.25)
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)
        server.shutdown()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch-pid", type=int, required=True)
    args = parser.parse_args()
    server = None
    for _ in range(20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", 8766), Handler)
            break
        except OSError:
            time.sleep(0.25)
    if server is None:
        return
    threading.Thread(target=watch_process, args=(server, args.watch_pid), daemon=True).start()
    server.serve_forever(poll_interval=0.25)
    server.server_close()


if __name__ == "__main__":
    main()
