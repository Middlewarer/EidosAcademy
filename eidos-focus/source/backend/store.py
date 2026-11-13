"""Compatibility layer for the legacy Eidos progress.json.

Unknown keys are always preserved. New focus data lives under ``focus_os`` so the
Tkinter app can continue to read and write the same file.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import shutil
import tempfile
import threading
import time
import sys
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

DEFAULT_STATE = Path.home() / ".eidos_learning_tracker" / "progress.json"
TRACKS = [
    ("python", "Python", "#8df5c7"), ("algorithms", "Алгоритмы", "#a997ff"),
    ("git", "Git", "#f0bd6b"), ("linux", "Linux", "#7eb7ff"),
    ("sql", "SQL", "#e999ae"), ("http", "HTTP & API", "#7fe1ef"),
    ("testing", "Тестирование", "#c8e171"), ("django", "Django", "#65c294"),
    ("docker", "Docker", "#6ba9ef"), ("async", "Async Python", "#cb9dff"),
]


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class ConflictError(RuntimeError):
    pass


class EidosStore:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or os.environ.get("EIDOS_STATE_FILE", DEFAULT_STATE)).expanduser().resolve()
        self.lock = threading.RLock()
        self._hash: str | None = None
        self.data: dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        with self.lock:
            raw = self.path.read_bytes() if self.path.exists() else None
            if raw:
                value = json.loads(raw.decode("utf-8-sig"))
                if not isinstance(value, dict):
                    raise ValueError("progress.json должен содержать JSON-объект")
                self.data = value
            else:
                self.data = {}
            self._hash = hashlib.sha256(raw).hexdigest() if raw is not None else None
            self._defaults()

    def _defaults(self) -> None:
        for key, value in {
            "completed": [], "prompt_ready": [], "task_records": {}, "work_seconds": {},
            "pomodoro_sessions": {}, "daily_target_hours": 6, "pomodoro_preset": "50/10",
            "interview_sessions": [], "daily_quests": {}, "career_actions": {},
            "verification_records": {}, "applications": [], "project_records": {},
            "career_profile": {}, "resume_checklist": {},
        }.items():
            self.data.setdefault(key, deepcopy(value))
        focus = self.data.setdefault("focus_os", {})
        focus.setdefault("version", 1)
        focus.setdefault("daily_missions", {})
        focus.setdefault("commitments", {})
        focus.setdefault("focus_sessions", [])
        focus.setdefault("parking_lot", {})
        # The native Focus app starts at the user's preferred 60/10 rhythm.
        # Once saved, these values are independent and always preserved.
        preset_focus, preset_break = 60, 10
        settings = focus.setdefault("pomodoro_settings", {})
        settings.setdefault("focus_minutes", preset_focus)
        settings.setdefault("break_minutes", preset_break)
        settings.setdefault("ambient_sound", "none")
        settings.setdefault("ambient_volume", 35)
        settings.setdefault("auto_start_break", True)

    def save(self) -> None:
        with self.lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            current = self.path.read_bytes() if self.path.exists() else None
            disk_hash = hashlib.sha256(current).hexdigest() if current is not None else None
            if disk_hash != self._hash:
                raise ConflictError("progress.json изменён другим приложением. Обновите страницу и повторите действие.")
            if current is not None:
                backup = self.path.with_name("progress.before_eidos_focus.json")
                if not backup.exists():
                    shutil.copy2(self.path, backup)
                shutil.copy2(self.path, self.path.with_name("progress.last-good.json"))
            encoded = json.dumps(self.data, ensure_ascii=False, indent=2).encode("utf-8")
            fd, tmp_name = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=self.path.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(encoded); stream.flush(); os.fsync(stream.fileno())
                os.replace(tmp_name, self.path)
            finally:
                if os.path.exists(tmp_name):
                    os.unlink(tmp_name)
            self._hash = hashlib.sha256(encoded).hexdigest()

    @property
    def today(self) -> str:
        return date.today().isoformat()

    def curriculum(self) -> tuple[list[dict[str, Any]], bool]:
        legacy_dir = os.environ.get("EIDOS_LEGACY_DIR")
        candidates = [Path(legacy_dir)] if legacy_dir else []
        executable_dir = Path(sys.executable).resolve().parent
        candidates += [
            self.path.parent,
            Path.cwd(),
            executable_dir.parent / "learning_tracker",
            executable_dir.parent.parent / "learning_tracker",
        ]
        for folder in candidates:
            source = folder / "mastery_curriculum.py"
            if not source.exists():
                continue
            try:
                folder_text = str(folder.resolve())
                if folder_text not in sys.path:
                    sys.path.insert(0, folder_text)
                spec = importlib.util.spec_from_file_location("eidos_mastery_curriculum", source)
                module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
                assert spec and spec.loader
                spec.loader.exec_module(module)
                return list(module.CURRICULUM), True
            except Exception:
                continue
        return [], False

    def track_summary(self) -> tuple[list[dict[str, Any]], bool]:
        curriculum, loaded = self.curriculum()
        completed = set(map(str, self.data.get("completed", [])))
        records = self.data.get("task_records", {})
        summaries = []
        for track_id, title, color in TRACKS:
            definition = next((x for x in curriculum if x.get("id") == track_id), None)
            if definition:
                task_ids = [str(task.get("id")) for topic in definition.get("topics", []) for task in topic.get("tasks", [])]
                title = definition.get("title", title)
            else:
                task_ids = [task_id for task_id in set(completed) | set(map(str, records)) if task_id == track_id or task_id.startswith((track_id + "-", track_id + "_", track_id + "."))]
            summaries.append({"id": track_id, "title": title, "done": sum(x in completed for x in task_ids), "total": len(task_ids), "color": color})
        return summaries, loaded

    def learning_tracks(self) -> dict[str, Any]:
        """Return a lightweight curriculum index without the very large prompts."""
        self.reload()
        curriculum, loaded = self.curriculum()
        completed = set(map(str, self.data.get("completed", [])))
        tracks = []
        for definition in curriculum:
            topics = []
            for topic in definition.get("topics", []):
                task_ids = [str(task.get("id", "")) for task in topic.get("tasks", [])]
                done = sum(task_id in completed for task_id in task_ids)
                topics.append({
                    "id": str(topic.get("id", "")),
                    "number": int(topic.get("number", 0) or 0),
                    "title": str(topic.get("title", "")),
                    "done": done,
                    "total": len(task_ids),
                    "has_exam": isinstance(topic.get("exam"), dict),
                })
            tracks.append({
                "id": str(definition.get("id", "")),
                "number": int(definition.get("number", 0) or 0),
                "title": str(definition.get("title", "")),
                "goal": str(definition.get("goal", "")),
                "color": str(definition.get("color", "#8df5c7")),
                "topics": topics,
                "done": sum(topic["done"] for topic in topics),
                "total": sum(topic["total"] for topic in topics),
            })
        return {"loaded": loaded, "tracks": tracks}

    def topic_detail(self, track_id: str, topic_id: str) -> dict[str, Any]:
        """Return one real Eidos topic, including prompts for the separate Prompt Lab."""
        self.reload()
        curriculum, loaded = self.curriculum()
        definition = next((item for item in curriculum if str(item.get("id")) == track_id), None)
        if not definition:
            raise ValueError("Учебный трек не найден")
        topic = next((item for item in definition.get("topics", []) if str(item.get("id")) == topic_id), None)
        if not topic:
            raise ValueError("Тема не найдена")
        completed = set(map(str, self.data.get("completed", [])))
        tasks = []
        for task in topic.get("tasks", []):
            task_id = str(task.get("id", ""))
            tasks.append({
                "id": task_id,
                "title": str(task.get("title", "")),
                "label": str(task.get("label", "ЗАДАЧА")),
                "kind": str(task.get("kind", "practice")),
                "statement": str(task.get("statement") or task.get("description") or ""),
                "deliverable": str(task.get("deliverable", "")),
                "example": str(task.get("example", "")),
                "difficulty": str(task.get("difficulty", "")),
                "minutes": int(task.get("minutes", 0) or 0),
                "artifact": str(task.get("artifact", "")),
                "external_url": str(task.get("external_url", "")),
                "done": task_id in completed,
            })
        exam = topic.get("exam") if isinstance(topic.get("exam"), dict) else None
        return {
            "loaded": loaded,
            "track": {"id": track_id, "title": str(definition.get("title", "")), "goal": str(definition.get("goal", "")), "color": str(definition.get("color", "#8df5c7"))},
            "topic": {
                "id": topic_id,
                "number": int(topic.get("number", 0) or 0),
                "title": str(topic.get("title", "")),
                "theory": str(topic.get("theory", "")),
                "pitfall": str(topic.get("pitfall", "")),
                "mastery": str(topic.get("mastery", "")),
                "practice_links": list(topic.get("practice_links", [])),
                "tasks": tasks,
                "mentor_prompt": str(topic.get("mentor_prompt", "")),
                "exam": ({
                    "title": str(exam.get("title", "")),
                    "description": str(exam.get("description", "")),
                    "minutes": int(exam.get("minutes", 0) or 0),
                    "exam_prompt": str(exam.get("exam_prompt", "")),
                } if exam else None),
            },
        }

    def _resume_percent(self) -> int:
        checklist = self.data.get("resume_checklist", {})
        if isinstance(checklist, dict) and checklist:
            values = list(checklist.values())
            done = sum(bool(v.get("done") if isinstance(v, dict) else v) for v in values)
            return round(done / len(values) * 100)
        records = self.data.get("resume_track", {}).get("records", {}) if isinstance(self.data.get("resume_track"), dict) else {}
        if records:
            return round(sum(bool(v.get("completed") or v.get("done")) for v in records.values()) / len(records) * 100)
        return 0

    def _interview_score(self) -> int:
        scores = []
        for session in self.data.get("interview_sessions", []):
            if not isinstance(session, dict): continue
            for key in ("score", "percent", "total_score"):
                if isinstance(session.get(key), (int, float)):
                    scores.append(float(session[key])); break
        return round(sum(scores) / len(scores)) if scores else 0

    def _streak(self) -> int:
        active = {k for k, v in self.data.get("work_seconds", {}).items() if int(v or 0) > 0}
        active |= {str(x.get("date")) for x in self.data["focus_os"]["focus_sessions"] if x.get("completed")}
        count, cursor = 0, date.today()
        if cursor.isoformat() not in active:
            cursor -= timedelta(days=1)
        while cursor.isoformat() in active:
            count += 1; cursor -= timedelta(days=1)
        return count

    def dashboard(self) -> dict[str, Any]:
        self.reload()
        tracks, curriculum_loaded = self.track_summary()
        total_tasks = sum(int(track.get("total", 0)) for track in tracks)
        done_tasks = sum(int(track.get("done", 0)) for track in tracks)
        try:
            start_date = date.fromisoformat(str(self.data.get("start_date")))
            target_date = date.fromisoformat(str(self.data.get("target_date")))
        except (TypeError, ValueError):
            start_date = date.today()
            target_date = start_date + timedelta(days=90)
        duration_days = max(1, (target_date - start_date).days + 1)
        elapsed_days = max(0, min(duration_days, (date.today() - start_date).days + 1))
        expected_tasks = round(total_tasks * elapsed_days / duration_days) if total_tasks else 0
        gap_tasks = max(0, expected_tasks - done_tasks)
        remaining_days = max(0, (target_date - date.today()).days + 1)
        pace_status = "behind" if gap_tasks >= 3 else ("ahead" if done_tasks >= expected_tasks + 3 else "on_track")
        start_week = date.today() - timedelta(days=date.today().weekday())
        applications = self.data.get("applications", [])
        apps_week = sum(1 for x in applications if str(x.get("created_at", ""))[:10] >= start_week.isoformat())
        heatmap = []
        for offset in range(34, -1, -1):
            day = (date.today() - timedelta(days=offset)).isoformat()
            heatmap.append({"date": day, "minutes": int(self.data.get("work_seconds", {}).get(day, 0)) // 60})
        mission = self.data["focus_os"]["daily_missions"].get(self.today, {"items": []})
        commitment = self.data["focus_os"]["commitments"].get(self.today, {})
        commitment = {"outcome": "", "deadline": "18:00", "focus_minutes": 150, "signed": False, **commitment}
        return {
            "date": self.today, "state_path": str(self.path), "mission": mission, "commitment": commitment,
            "metrics": {
                "focus_minutes": int(self.data["work_seconds"].get(self.today, 0)) // 60,
                "target_minutes": int(self.data.get("daily_target_hours", 6)) * 60,
                "streak": self._streak(), "completed_tasks": len(self.data.get("completed", [])),
                "project_steps": sum(len(value) for value in self.data.get("project_records", {}).values() if isinstance(value, dict)),
                "applications_week": apps_week, "interview_score": self._interview_score(),
                "resume_percent": self._resume_percent(),
            },
            "pace": {
                "status": pace_status,
                "actual_tasks": done_tasks,
                "expected_tasks": expected_tasks,
                "total_tasks": total_tasks,
                "gap_tasks": gap_tasks,
                "actual_percent": round(done_tasks / total_tasks * 100) if total_tasks else 0,
                "expected_percent": round(expected_tasks / total_tasks * 100) if total_tasks else 0,
                "days_remaining": remaining_days,
                "target_date": target_date.isoformat(),
                "tasks_per_day_needed": math.ceil(max(0, total_tasks - done_tasks) / max(1, remaining_days)),
            },
            "pomodoro": deepcopy(self.data["focus_os"]["pomodoro_settings"]),
            "tracks": tracks, "applications": list(reversed(applications[-20:])), "heatmap": heatmap,
            "compatibility": {"learning_model": self.data.get("learning_model"), "career_model": self.data.get("career_model"), "curriculum_loaded": curriculum_loaded},
        }

    def set_mission(self, items: list[dict[str, Any]]) -> None:
        clean = []
        for item in items[:3]:
            title = str(item.get("title", "")).strip()[:180]
            if title:
                clean.append({"id": str(item.get("id") or f"mission-{time.time_ns()}"), "title": title, "kind": str(item.get("kind", "learn"))[:20], "done": bool(item.get("done"))})
        self.data["focus_os"]["daily_missions"][self.today] = {"items": clean, "updated_at": now()}
        self.save()

    def set_commitment(self, value: dict[str, Any]) -> None:
        self.data["focus_os"]["commitments"][self.today] = {
            "outcome": str(value.get("outcome", "")).strip()[:240], "deadline": str(value.get("deadline", "18:00"))[:5],
            "focus_minutes": max(25, min(720, int(value.get("focus_minutes", 150)))),
            "signed": True, "signed_at": now(),
        }
        self.save()

    def set_pomodoro_settings(self, value: dict[str, Any]) -> None:
        focus_minutes = max(10, min(180, int(value.get("focus_minutes", 60))))
        break_minutes = max(1, min(60, int(value.get("break_minutes", 10))))
        sound = str(value.get("ambient_sound", "none"))
        if sound not in {"none", "rain", "fire", "ocean"}:
            sound = "none"
        self.data["focus_os"]["pomodoro_settings"] = {
            "focus_minutes": focus_minutes,
            "break_minutes": break_minutes,
            "ambient_sound": sound,
            "ambient_volume": max(0, min(100, int(value.get("ambient_volume", 35)))),
            "auto_start_break": bool(value.get("auto_start_break", True)),
        }
        self.data["pomodoro_preset"] = f"{focus_minutes}/{break_minutes}"
        self.save()

    def add_session(self, value: dict[str, Any]) -> None:
        elapsed = max(0, min(12 * 3600, int(value.get("elapsed_seconds", 0))))
        session = {"id": f"focus-{time.time_ns()}", "date": self.today, "task": str(value.get("task", ""))[:240], "elapsed_seconds": elapsed, "completed": bool(value.get("completed")), "ended_at": now()}
        self.data["focus_os"]["focus_sessions"].append(session)
        self.data["work_seconds"][self.today] = int(self.data["work_seconds"].get(self.today, 0)) + elapsed
        if session["completed"]:
            self.data["pomodoro_sessions"][self.today] = int(self.data["pomodoro_sessions"].get(self.today, 0)) + 1
        self.save()

    def add_application(self, value: dict[str, Any]) -> None:
        company, role = str(value.get("company", "")).strip(), str(value.get("role", "")).strip()
        if not company or not role: raise ValueError("Укажите компанию и позицию")
        stamp = datetime.now().isoformat(timespec="minutes")
        self.data["applications"].append({"id": f"app-{int(time.time()*1000)}", "company": company[:120], "role": role[:160], "url": "", "status": "saved", "note": "", "created_at": stamp, "updated_at": stamp})
        self.save()
