from __future__ import annotations

import json
import mimetypes
import os
import socket
import sys
import threading
import ctypes
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from store import ConflictError, EidosStore

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
DIST = ROOT / "web-dist"
STORE = EidosStore()


class TimerController:
    def __init__(self):
        self.lock = threading.RLock()
        self.running = False
        self.mode = "focus"
        self.task = ""
        self.started_at = 0.0
        self.segment_remaining = self.duration()
        self.remaining = self.segment_remaining

    def duration(self) -> int:
        settings = STORE.data.get("focus_os", {}).get("pomodoro_settings", {})
        key = "break_minutes" if self.mode == "break" else "focus_minutes"
        fallback = 10 if self.mode == "break" else 50
        return max(1, int(settings.get(key, fallback))) * 60

    def _current_remaining(self) -> int:
        if not self.running:
            return int(self.remaining)
        return max(0, int(self.segment_remaining - (time.monotonic() - self.started_at)))

    def _flush(self, completed: bool = False) -> None:
        if not self.running:
            if completed and self.mode == "focus":
                STORE.add_session({"task": self.task, "elapsed_seconds": 0, "completed": True})
            return
        current = self._current_remaining()
        elapsed = max(0, int(self.segment_remaining - current))
        self.remaining = current
        self.running = False
        if self.mode == "focus" and (elapsed or completed):
            STORE.add_session({"task": self.task, "elapsed_seconds": elapsed, "completed": completed})

    def _begin_mode(self, mode: str, running: bool = False) -> None:
        self.mode = mode
        self.remaining = self.duration()
        self.segment_remaining = self.remaining
        self.running = running
        if running:
            self.started_at = time.monotonic()

    def snapshot(self) -> dict:
        with self.lock:
            current = self._current_remaining()
            if self.running and current <= 0:
                previous_mode = self.mode
                self._flush(completed=previous_mode == "focus")
                if previous_mode == "focus":
                    auto = bool(STORE.data.get("focus_os", {}).get("pomodoro_settings", {}).get("auto_start_break", True))
                    self._begin_mode("break", running=auto)
                else:
                    self._begin_mode("focus", running=False)
                current = self.remaining
            settings = STORE.data.get("focus_os", {}).get("pomodoro_settings", {})
            return {"duration": self.duration(), "remaining": current, "running": self.running, "task": self.task, "mode": self.mode, "focus_minutes": int(settings.get("focus_minutes", 50)), "break_minutes": int(settings.get("break_minutes", 10))}

    def action(self, value: dict) -> dict:
        with self.lock:
            action = str(value.get("action", ""))
            task = str(value.get("task", "")).strip()[:240]
            if task:
                self.task = task
            if action == "start" and not self.running:
                if self.remaining <= 0 or self.remaining > self.duration():
                    self.remaining = self.duration()
                self.segment_remaining = self.remaining
                self.started_at = time.monotonic()
                self.running = True
            elif action == "pause":
                self._flush(completed=False)
            elif action == "reset":
                self._flush(completed=False)
                self.remaining = self.duration()
            elif action == "complete":
                previous_mode = self.mode
                self._flush(completed=previous_mode == "focus")
                if previous_mode == "focus":
                    auto = bool(STORE.data.get("focus_os", {}).get("pomodoro_settings", {}).get("auto_start_break", True))
                    self._begin_mode("break", running=auto)
                else:
                    self._begin_mode("focus", running=False)
            elif action not in {"start", "pause", "reset", "complete"}:
                raise ValueError("Неизвестное действие таймера")
            state = self.snapshot()
        return state


TIMER = TimerController()


def focus_existing_window() -> None:
    """Restore the existing native Eidos window on a second launch."""
    try:
        user32 = ctypes.windll.user32
        handle = user32.FindWindowW(None, "Eidos Focus")
        if handle:
            user32.ShowWindow(handle, 9)  # SW_RESTORE
            user32.SetForegroundWindow(handle)
    except Exception:
        pass


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[Eidos]", fmt % args)

    def send_json(self, value, status=200):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def body(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/dashboard": return self.send_json(STORE.dashboard())
        if path == "/api/timer": return self.send_json(TIMER.snapshot())
        if path == "/api/pomodoro-settings": return self.send_json(STORE.data.get("focus_os", {}).get("pomodoro_settings", {}))
        if path == "/api/learning": return self.send_json(STORE.learning_tracks())
        if path == "/api/topic":
            query = parse_qs(parsed.query)
            try:
                return self.send_json(STORE.topic_detail(query.get("track", [""])[0], query.get("topic", [""])[0]))
            except ValueError as exc:
                return self.send_json({"error": str(exc)}, 404)
        relative = "index.html" if path == "/" else path.lstrip("/")
        target = (DIST / relative).resolve()
        if DIST.resolve() not in target.parents and target != DIST.resolve(): return self.send_error(403)
        if not target.is_file(): target = DIST / "index.html"
        if not target.exists(): return self.send_json({"error": "Frontend не собран. Выполните npm install и npm run build."}, 503)
        body = target.read_bytes(); mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(200); self.send_header("Content-Type", mime); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def mutate(self, action):
        try:
            action(self.body()); self.send_json(STORE.dashboard())
        except ConflictError as exc: self.send_json({"error": str(exc)}, 409)
        except (ValueError, TypeError, json.JSONDecodeError) as exc: self.send_json({"error": str(exc)}, 400)
        except Exception as exc: self.send_json({"error": f"Не удалось сохранить: {exc}"}, 500)

    def do_PUT(self):
        path = urlparse(self.path).path
        if path == "/api/mission": return self.mutate(lambda body: STORE.set_mission(body.get("items", [])))
        if path == "/api/commitment": return self.mutate(STORE.set_commitment)
        if path == "/api/pomodoro-settings":
            def save_settings(body):
                STORE.set_pomodoro_settings(body)
                with TIMER.lock:
                    if not TIMER.running:
                        TIMER.remaining = TIMER.duration()
                        TIMER.segment_remaining = TIMER.remaining
            return self.mutate(save_settings)
        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/timer":
            try: return self.send_json(TIMER.action(self.body()))
            except ConflictError as exc: return self.send_json({"error": str(exc)}, 409)
            except (ValueError, TypeError, json.JSONDecodeError) as exc: return self.send_json({"error": str(exc)}, 400)
        if path == "/api/focus-session": return self.mutate(STORE.add_session)
        if path == "/api/applications": return self.mutate(STORE.add_application)
        self.send_error(404)


def main():
    if not DIST.exists():
        print("Frontend build not found. Run: npm install; npm run build", file=sys.stderr); raise SystemExit(2)
    # Double-clicking the shortcut while Eidos is already running should focus the
    # product, not fail with a second-server error.
    try:
        with socket.create_connection(("127.0.0.1", 8765), timeout=0.35):
            focus_existing_window()
            return
    except OSError:
        pass
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    url = "http://127.0.0.1:8765"
    print(f"Eidos Focus: {url}\nData: {STORE.path}")
    if "--server-only" in sys.argv:
        try: server.serve_forever()
        except KeyboardInterrupt: pass
        finally: server.server_close()
        return

    import webview

    class NativeApi:
        _main_window = None
        _widget_window = None
        _prompt_window = None

        def _position_widget(self):
            class Rect(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
            area = Rect()
            ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(area), 0)
            self._widget_window.move(area.right - 386, area.bottom - 196)

        def open_widget(self):
            self._position_widget()
            self._widget_window.show()

        def hide_widget(self):
            self._widget_window.hide()

        def show_main(self):
            self._main_window.show()
            self._main_window.restore()
            focus_existing_window()

        def open_prompt_lab(self, track_id="", topic_id=""):
            query = urlencode({"prompts": "1", "track": str(track_id), "topic": str(topic_id)})
            self._prompt_window.load_url(url + "/?" + query)
            self._prompt_window.show()
            self._prompt_window.restore()

        def hide_prompt_lab(self):
            self._prompt_window.hide()

    worker = threading.Thread(target=server.serve_forever, name="eidos-local-api", daemon=True)
    worker.start()
    storage = Path.home() / ".eidos_learning_tracker" / "webview"
    storage.mkdir(parents=True, exist_ok=True)
    native = NativeApi()
    native._main_window = webview.create_window(
        "Eidos Focus",
        url,
        js_api=native,
        width=1280,
        height=820,
        min_size=(980, 680),
        resizable=True,
        background_color="#090b0f",
        text_select=False,
        zoomable=False,
    )
    class Rect(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    work_area = Rect()
    ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(work_area), 0)
    native._widget_window = webview.create_window(
        "Eidos Pomodoro",
        url + "/?widget=1",
        js_api=native,
        width=368,
        height=178,
        x=work_area.right - 386,
        y=work_area.bottom - 196,
        min_size=(368, 178),
        resizable=False,
        frameless=True,
        easy_drag=False,
        shadow=True,
        on_top=True,
        hidden="--show-widget" not in sys.argv,
        background_color="#0c0f14",
        text_select=False,
        zoomable=False,
    )
    native._prompt_window = webview.create_window(
        "Eidos Prompt Lab",
        url + "/?prompts=1",
        js_api=native,
        width=820,
        height=760,
        min_size=(680, 580),
        resizable=True,
        hidden=True,
        background_color="#090b0f",
        text_select=True,
        zoomable=False,
    )
    try:
        webview.start(gui="edgechromium", debug=False, private_mode=False, storage_path=str(storage))
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__": main()
