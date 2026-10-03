"""Job Search OS: обучение, доказательства навыков и воронка найма."""

from __future__ import annotations

import json
import math
import os
import shutil
import tempfile
import hashlib
import time
import tkinter as tk
import webbrowser
import weakref
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import messagebox, ttk

from daily_plan import TRACK_PRIORITY, build_daily_plan
from career_readiness import (
    PROJECTS, RESUME_CHECKLIST, VERIFICATION_SCORE,
    readiness_summary, topic_studied,
)
from manual_applications import ApplicationsWindow
from preparation import discipline, migrate, CHECKPOINTS
from interview_lab import InterviewLabWindow
from mastery_curriculum import CURRICULUM, all_task_ids
from progress_insights import calendar_day, completed_topics, interview_prompt, overdue_tasks, weekly_summary


BG = "#07111F"
PANEL = "#0E1B2E"
PANEL_2 = "#152842"
TEXT = "#F3F8FF"
MUTED = "#8FA3BC"
BORDER = "#233B57"
ACCENT = "#2DD4BF"
SUCCESS = "#5EE6A8"
WARNING = "#F8C15C"
DANGER = "#FF718B"
BLUE = "#55A7FF"
FONT = "Segoe UI"

APP_DIR = Path(__file__).resolve().parent
WORKSPACE = APP_DIR.parent / "learning_labs"
STATE_FILE = Path(os.environ.get("EIDOS_STATE_FILE", str(Path.home() / ".eidos_learning_tracker" / "progress.json")))
SCROLL_FRAMES = []
CAREER_TRACK_ORDER = {
    track_id: index for index, track_id in enumerate(
        ("python", "algorithms", "git", "linux", "sql", "http", "testing", "django", "docker", "async")
    )
}


def route_mousewheel(event):
    """Направляет колесо и жест тачпада в область под курсором."""
    try:
        widget = event.widget.winfo_toplevel().winfo_containing(event.x_root, event.y_root)
    except tk.TclError:
        return None
    alive = []
    candidates = []
    for reference in SCROLL_FRAMES:
        frame = reference()
        if frame is None:
            continue
        try:
            if not frame.winfo_exists():
                continue
        except tk.TclError:
            continue
        alive.append(reference)
        current = widget
        distance = 0
        while current is not None:
            if current is frame:
                candidates.append((distance, frame))
                break
            current = getattr(current, "master", None)
            distance += 1
    SCROLL_FRAMES[:] = alive
    if not candidates or not event.delta:
        return None
    frame = min(candidates, key=lambda item: item[0])[1]
    units = max(1, abs(event.delta) // 120)
    frame.canvas.yview_scroll(-units if event.delta > 0 else units, "units")
    return "break"


def enable_dpi_awareness():
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


class Store:
    def __init__(self, path: Path):
        self.path = path
        self.data = self.load()

    def load(self):
        try:
            raw = self.path.read_bytes()
        except FileNotFoundError:
            raw = None
        self._disk_hash = hashlib.sha256(raw).hexdigest() if raw is not None else None
        if raw is None:
            payload = {}
        else:
            try:
                payload = json.loads(raw.decode("utf-8-sig"))
                if not isinstance(payload, dict):
                    raise ValueError("Неверный формат прогресса")
            except (ValueError, UnicodeError) as exc:
                raise RuntimeError(f"Не удалось прочитать прогресс {self.path}. Файл не изменён. Резервная копия: progress.last-good.json.") from exc
        if payload.get("learning_model") != 6:
            payload.setdefault("legacy_completed", [])
            payload["legacy_completed"] = sorted(set(payload["legacy_completed"]) | set(payload.get("completed", [])))
            payload["completed"] = []
            payload["prompt_ready"] = []
            payload["task_records"] = {}
            payload["learning_model"] = 6
        payload.setdefault("completed", [])
        payload.setdefault("prompt_ready", [])
        payload.setdefault("task_records", {})
        payload.setdefault("work_seconds", {})
        payload.setdefault("pomodoro_sessions", {})
        payload.setdefault("daily_target_hours", 6)
        payload.setdefault("pomodoro_preset", "50/10")
        payload.setdefault("interview_sessions", [])
        payload.setdefault("daily_quests", {})
        payload.setdefault("career_actions", {})
        payload.setdefault("verification_records", {})
        payload.setdefault("applications", [])
        payload.setdefault("project_records", {})
        payload.setdefault("career_profile", {})
        payload.setdefault("resume_checklist", {})
        if payload.get("career_model") != 1:
            payload["career_model"] = 1
            payload["daily_target_hours"] = 8
        self.needs_preparation_save = migrate(payload)
        return payload

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        current = self.path.read_bytes() if self.path.exists() else None
        disk_hash = hashlib.sha256(current).hexdigest() if current is not None else None
        if disk_hash != self._disk_hash:
            raise RuntimeError("Прогресс изменён другим экземпляром приложения. Перезапусти это окно, чтобы не перезаписать новые данные.")
        backup = self.path.with_name("progress.before_job_search_os.json")
        if self.path.exists() and not backup.exists():
            shutil.copy2(self.path, backup)
        if current is not None:
            shutil.copy2(self.path, self.path.with_name("progress.last-good.json"))
        encoded = json.dumps(self.data, ensure_ascii=False, indent=2).encode("utf-8")
        fd, name = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, self.path)
        finally:
            if os.path.exists(name):
                os.unlink(name)
        self._disk_hash = hashlib.sha256(encoded).hexdigest()

    def solved(self, task_id):
        return task_id in set(self.data["completed"])

    def mark_prompt(self, topic_id):
        if topic_id not in self.data["prompt_ready"]:
            self.data["prompt_ready"].append(topic_id)
        self.save()

    def record(self, task_id, status, path, note):
        records = self.data["task_records"].setdefault(task_id, {"attempts": []})
        records["path"] = str(path) if path else ""
        records["status"] = status
        records["note"] = note.strip()
        records["updated_at"] = datetime.now().isoformat(timespec="minutes")
        records["attempts"].append({"status": status, "at": records["updated_at"], "note": note.strip()})
        completed = set(self.data["completed"])
        if status == "solved":
            completed.add(task_id)
        else:
            completed.discard(task_id)
        self.data["completed"] = sorted(completed)
        self.save()

    def complete_quest(self, quest_key):
        self.data["daily_quests"][quest_key] = datetime.now().isoformat(timespec="minutes")
        self.save()

    def complete_career_action(self, action_key):
        self.data["career_actions"][action_key] = datetime.now().isoformat(timespec="minutes")
        self.save()

    def save_verification(self, topic_id, score, evidence, note):
        record = self.data["verification_records"].setdefault(topic_id, {"attempts": []})
        attempt = {
            "score": score,
            "evidence": evidence.strip(),
            "note": note.strip(),
            "at": datetime.now().isoformat(timespec="minutes"),
        }
        attempt["status"] = "verified" if score >= VERIFICATION_SCORE and len(evidence.strip()) >= 30 else "retry"
        record.update(attempt)
        record["attempts"].append(attempt)
        self.save()

    def save_project_evidence(self, project_id, milestone_id, evidence):
        project = self.data["project_records"].setdefault(project_id, {})
        project[milestone_id] = {
            "evidence": evidence.strip(),
            "at": datetime.now().isoformat(timespec="minutes"),
        }
        self.save()

    def add_application(self, company, role, url, status, note, **extra):
        item = {
            "id": f'app-{int(time.time() * 1000)}',
            "company": company.strip(),
            "role": role.strip(),
            "url": url.strip(),
            "status": status,
            "note": note.strip(),
            "created_at": datetime.now().isoformat(timespec="minutes"),
            "updated_at": datetime.now().isoformat(timespec="minutes"),
            **extra,
        }
        self.data["applications"].append(item)
        self.save()
        return item

    def update_application_status(self, application_id, status):
        for item in self.data["applications"]:
            if item.get("id") == application_id:
                item["status"] = status
                item["updated_at"] = datetime.now().isoformat(timespec="minutes")
                break
        self.save()

    def save_cover_letter(self, application_id, text):
        for item in self.data["applications"]:
            if item.get("id") == application_id:
                item["cover_letter"] = text.strip()
                item["updated_at"] = datetime.now().isoformat(timespec="minutes")
                break
        self.save()


class ScrollFrame(tk.Frame):
    def __init__(self, master, bg=BG, width=None):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, width=width)
        self.bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.bar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.bar.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        SCROLL_FRAMES.append(weakref.ref(self))

    def top(self):
        self.canvas.yview_moveto(0)


def button(parent, text, command, *, primary=False, width=None):
    return tk.Button(
        parent, text=text, command=command, width=width,
        bg=ACCENT if primary else PANEL_2, fg=TEXT,
        activebackground="#9387FF" if primary else "#22304D", activeforeground=TEXT,
        relief="flat", bd=0, cursor="hand2", padx=16, pady=10,
        font=(FONT, 10, "bold"),
    )


def label(parent, text, *, size=10, color=TEXT, bold=False, bg=None, wrap=None, pack=None):
    widget = tk.Label(parent, text=text, bg=bg or parent.cget("bg"), fg=color,
                      font=(FONT, size, "bold" if bold else "normal"),
                      justify="left", anchor="w", wraplength=wrap)
    if pack is not None:
        widget.pack(**pack)
    return widget


class LearningApp(tk.Tk):
    def __init__(self, state_file=None):
        super().__init__()
        self.title("Job Search OS")
        self.geometry("1180x790")
        self.minsize(980, 700)
        self.configure(bg=BG)
        style = ttk.Style(self)
        style.configure(
            "Focus.Horizontal.TProgressbar",
            troughcolor="#202B45", background=ACCENT,
            bordercolor="#202B45", lightcolor=ACCENT, darkcolor=ACCENT,
            thickness=8,
        )
        self.store = Store(state_file or STATE_FILE)
        self.windows = {}
        self.timer_running = False
        self.timer_started = None
        self.timer_after = None
        self.timer_mode = "focus"
        self.timer_remaining = self.pomodoro_durations()["focus"]
        self.timer_segment_started = self.timer_remaining
        self.bind_all("<MouseWheel>", route_mousewheel, add="+")
        self.build()

    def build(self):
        metrics = readiness_summary(self.store)
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=36, pady=(24, 14))
        left = tk.Frame(header, bg=BG)
        left.pack(side="left", fill="x", expand=True)
        label(left, "JOB SEARCH OS · PYTHON BACKEND", size=10, color=ACCENT, bold=True, pack={"anchor": "w"})
        label(left, "Цель: работа к 15 декабря", size=27, bold=True, pack={"anchor": "w", "pady": (5, 4)})
        label(left, "Старт 02.10 · HARD MODE · 9 часов работы, перерывы отдельно · воскресенье — отдых.",
              size=11, color=MUTED, pack={"anchor": "w"})
        label(left, discipline(), size=10, color=WARNING, wrap=720, pack={"anchor": "w", "pady": (5, 0)})

        timer = tk.Frame(header, bg=PANEL, padx=18, pady=13, highlightbackground=BORDER, highlightthickness=1)
        timer.pack(side="right")
        label(timer, f'ДО ДЕДЛАЙНА · {metrics["days_left"]} ДНЕЙ', size=8, color=WARNING, bold=True,
              pack={"anchor": "w"})
        self.timer_label = label(timer, "0 ч 00 мин / 6 ч", size=15, bold=True,
                                 pack={"anchor": "w", "pady": (3, 5)})
        self.timer_status_label = label(timer, "Фокус готов · 50:00", size=9, color=MUTED,
                                        pack={"anchor": "w", "pady": (0, 8)})
        self.timer_progress = ttk.Progressbar(timer, maximum=100, value=0, length=245,
                                               style="Focus.Horizontal.TProgressbar")
        self.timer_progress.pack(fill="x", pady=(0, 9))
        button(timer, "Открыть Pomodoro →", self.open_pomodoro, primary=True).pack(fill="x")
        self.update_timer()

        readiness = tk.Frame(self, bg=BG)
        readiness.pack(fill="x", padx=32, pady=(0, 14))
        kpis = [
            (f'{metrics["studied"]}/{metrics["total_topics"]}', "тем завершено", ACCENT),
            (str(metrics["verified"]), "тем проверено", SUCCESS),
            (f'{metrics["project_done"]}/{metrics["project_total"]}', "проектных доказательств", BLUE),
            (f'{metrics["interview"]}/100', "средний балл интервью", WARNING),
            (f'{metrics["overall"]}%', "готовность к найму", TEXT),
        ]
        for index, (value, caption, color) in enumerate(kpis):
            readiness.grid_columnconfigure(index, weight=1, uniform="career-kpi")
            card = tk.Frame(readiness, bg=PANEL, padx=14, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=index, sticky="nsew", padx=4)
            label(card, value, size=18, color=color, bold=True, pack={"anchor": "w"})
            label(card, caption, size=8, color=MUTED, wrap=160, pack={"anchor": "w", "pady": (3, 0)})

        priority = tk.Frame(self, bg="#10253A", padx=18, pady=12,
                            highlightbackground=ACCENT, highlightthickness=1)
        priority.pack(fill="x", padx=36, pady=(0, 12))
        if metrics["knowledge"] < 100:
            priority_title = "P0 · Продолжить обязательный учебный маршрут"
            priority_text = "Сначала фундамент и backend-база по порядку. HH ограничен короткой разминкой и не забирает учебный блок."
            priority_command = self.open_today
            priority_button = "Открыть сегодня"
        elif metrics["project_done"] < metrics["project_total"]:
            priority_title = "P0 · Подтвердить знания проектом"
            priority_text = "Закрой следующий проектный milestone с тестом, выводом команды или другим воспроизводимым доказательством."
            priority_command = self.open_projects
            priority_button = "Открыть проекты"
        elif metrics["interview"] < 85:
            priority_title = "P0 · Поднять техническое интервью до 85+"
            priority_text = "Проверь знания без подсказок и преврати ошибки в точечное повторение."
            priority_command = self.open_interview
            priority_button = "Открыть интервью"
        elif metrics["resume"] < 100:
            priority_title = "P0 · Упаковать доказанные навыки"
            priority_text = "Обнови резюме только фактами, которые уже подтверждены темами и проектами."
            priority_command = self.open_resume_lab
            priority_button = "Открыть резюме"
        else:
            priority_title = "P0 · Усиливать слабейший технический блок"
            priority_text = "Сравни учебный прогресс, проектные доказательства и интервью — работай над самым слабым доказуемым навыком."
            priority_command = self.open_weekly_report
            priority_button = "Открыть отчёт"
        info = tk.Frame(priority, bg="#10253A")
        info.pack(side="left", fill="x", expand=True)
        label(info, priority_title, size=11, color=ACCENT, bold=True, bg="#10253A", pack={"anchor": "w"})
        label(info, priority_text, size=9, color=MUTED, bg="#10253A", wrap=820,
              pack={"anchor": "w", "pady": (3, 0)})
        button(priority, priority_button, priority_command, primary=True).pack(side="right", padx=(12, 0))

        navigation = tk.Frame(self, bg=BG)
        navigation.pack(fill="x", padx=36, pady=(0, 12))
        button(navigation, "Сегодня", self.open_today, primary=True).pack(side="left", padx=(0, 8))
        button(navigation, "Матрица навыков", self.open_skill_matrix).pack(side="left", padx=(0, 8))
        button(navigation, "Проекты", self.open_projects).pack(side="left", padx=(0, 8))
        button(navigation, "Резюме", self.open_resume_lab).pack(side="left", padx=(0, 8))
        button(navigation, "Отклики", self.open_applications).pack(side="left", padx=(0, 8))
        button(navigation, "Собеседования", self.open_interview).pack(side="left", padx=(0, 8))
        button(navigation, "Отчёт", self.open_weekly_report).pack(side="left")

        self.daily_card()

        body = ScrollFrame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        grid = body.inner
        for column in range(2):
            grid.grid_columnconfigure(column, weight=1, uniform="tracks")
        ordered_tracks = sorted(CURRICULUM, key=lambda item: CAREER_TRACK_ORDER[item["id"]])
        label(grid, "БАЗА ЗНАНИЙ ПО НАПРАВЛЕНИЯМ", size=9, color=MUTED, bold=True,
              pack=None).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 6))
        for index, track in enumerate(ordered_tracks):
            self.track_card(grid, track, index // 2 + 1, index % 2)

    def track_card(self, parent, track, row, column):
        card = tk.Frame(parent, bg=PANEL, padx=22, pady=18, highlightbackground=BORDER, highlightthickness=1)
        card.grid(row=row, column=column, sticky="nsew", padx=8, pady=8)
        topics_done = sum(topic_studied(self.store, topic) for topic in track["topics"])
        top = tk.Frame(card, bg=PANEL)
        top.pack(fill="x")
        tk.Label(top, text=track["icon"], bg=track["color"], fg="#08101C", width=4, height=2,
                 font=(FONT, 10, "bold")).pack(side="left", padx=(0, 14))
        names = tk.Frame(top, bg=PANEL)
        names.pack(side="left", fill="x", expand=True)
        label(names, track["title"], size=15, bold=True, pack={"anchor": "w"})
        label(names, f'{topics_done}/24 тем завершено', color=MUTED,
              pack={"anchor": "w", "pady": (3, 0)})
        ttk.Progressbar(card, maximum=24, value=topics_done).pack(fill="x", pady=(16, 14))
        label(card, track["goal"], color=MUTED, wrap=470,
              pack={"anchor": "w", "fill": "x", "pady": (0, 14)})
        button(card, "Открыть направление →", lambda t=track: self.open_track(t), primary=True).pack(anchor="e")

    def daily_card(self):
        today = datetime.now().date()
        day, upcoming = calendar_day(today)
        card = tk.Frame(self, bg="#151F37", padx=22, pady=16, highlightbackground="#394A72", highlightthickness=1)
        card.pack(fill="x", padx=36, pady=(0, 16))
        left = tk.Frame(card, bg="#151F37")
        left.pack(side="left", fill="x", expand=True)
        prefix = "ПЛАН НА СЕГОДНЯ" if day else "СЕГОДНЯ — ДЕНЬ БЕЗ НОВЫХ ТЕМ"
        label(left, prefix, size=8, color="#8F82FF", bold=True, bg="#151F37", pack={"anchor": "w"})
        if day:
            names = "  +  ".join(topic["title"] for _track, topic in day["topics"]) or "Пробные интервью, повтор ошибок, ручной поиск"
            hours, minutes = divmod(day["minutes"], 60)
            done = sum(self.store.solved(task_id) for task_id in day["task_ids"])
            label(left, f'День {day["number"]} · {done}/{len(day["task_ids"])} задач', size=14, bold=True,
                  bg="#151F37", pack={"anchor": "w", "pady": (3, 2)})
            label(left, f'Этап: {day["phase"]["title"]}', color=ACCENT, bg="#151F37",
                  pack={"anchor": "w", "pady": (0, 2)})
            label(left, f"{names} · около {hours} ч {minutes:02} мин, включая повторение",
                  color=MUTED, bg="#151F37", wrap=720, pack={"anchor": "w"})
        elif upcoming:
            label(left, today.strftime("%d.%m.%Y"), size=14, bold=True, bg="#151F37",
                  pack={"anchor": "w", "pady": (3, 2)})
            label(left, f'Следующий учебный день: {upcoming["date"].strftime("%d.%m.%Y")}. Можно закрыть долги или отдохнуть.',
                  color=MUTED, bg="#151F37", wrap=720, pack={"anchor": "w"})
        else:
            label(left, "Учебный план завершён", size=14, bold=True, bg="#151F37",
                  pack={"anchor": "w", "pady": (3, 2)})
            label(left, "Открой недельный отчёт или режим собеседования для проверки готовности.",
                  color=MUTED, bg="#151F37", wrap=720, pack={"anchor": "w"})
        actions = tk.Frame(card, bg="#151F37")
        actions.pack(side="right", padx=(18, 0))
        button(actions, "Весь план", self.open_plan).pack(side="left", padx=(0, 8))
        button(actions, "Открыть сегодня →", self.open_today, primary=True).pack(side="left")

    def open_track(self, track, topic_id=None):
        current = self.windows.get(track["id"])
        if current and current.winfo_exists():
            if topic_id:
                current.open_topic_id(topic_id)
            current.lift()
            current.focus_force()
            return
        window = TrackWindow(self, track, self.store, self.refresh)
        self.windows[track["id"]] = window
        if topic_id:
            window.open_topic_id(topic_id)

    def open_plan(self):
        current = self.windows.get("daily-plan")
        if current and current.winfo_exists():
            current.lift()
            return
        self.windows["daily-plan"] = PlanWindow(self, self.store, self.open_track)

    def open_today(self):
        current = self.windows.get("today")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            current.focus_force()
            return
        self.windows["today"] = TodayWindow(self, self.store, self.open_track, self.open_pomodoro)

    def open_skill_matrix(self):
        current = self.windows.get("skill-matrix")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            return
        self.windows["skill-matrix"] = SkillMatrixWindow(self, self.store, self.open_track, self.refresh)

    def open_projects(self):
        current = self.windows.get("projects")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            return
        self.windows["projects"] = ProjectProofWindow(self, self.store, self.refresh)

    def open_resume_lab(self):
        current = self.windows.get("resume-lab")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            return
        self.windows["resume-lab"] = ResumeLabWindow(self, self.store, self.refresh)

    def open_applications(self):
        current = self.windows.get("applications")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            return
        self.windows["applications"] = ApplicationsWindow(self, self.store, self.refresh)

    def open_interview(self):
        current = self.windows.get("interview")
        if current and current.winfo_exists():
            current.lift()
            current.focus_force()
            return
        self.windows["interview"] = InterviewLabWindow(self, self.store)

    def open_weekly_report(self):
        current = self.windows.get("weekly-report")
        if current and current.winfo_exists():
            current.render()
            current.lift()
            current.focus_force()
            return
        self.windows["weekly-report"] = WeeklyReportWindow(self, self.store)

    def refresh(self):
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Toplevel):
                widget.destroy()
        self.build()

    def open_pomodoro(self):
        current = self.windows.get("pomodoro")
        if current and current.winfo_exists():
            current.lift()
            current.focus_force()
            return
        self.windows["pomodoro"] = PomodoroWindow(self)

    def today_key(self):
        return datetime.now().date().isoformat()

    def pomodoro_durations(self):
        preset = self.store.data.get("pomodoro_preset", "50/10")
        if preset == "25/5":
            return {"focus": 25 * 60, "short_break": 5 * 60, "long_break": 15 * 60}
        return {"focus": 50 * 60, "short_break": 10 * 60, "long_break": 30 * 60}

    def today_sessions(self):
        return int(self.store.data["pomodoro_sessions"].get(self.today_key(), 0))

    def set_daily_target(self, hours):
        self.store.data["daily_target_hours"] = hours
        self.store.save()
        self.update_timer()

    def set_pomodoro_preset(self, preset):
        self.pause_timer()
        self.store.data["pomodoro_preset"] = preset
        self.store.save()
        self.timer_mode = "focus"
        self.timer_remaining = self.pomodoro_durations()["focus"]
        self.timer_segment_started = self.timer_remaining
        self.update_timer()

    def toggle_timer(self):
        if self.timer_running:
            self.pause_timer()
        else:
            self.timer_running = True
            self.timer_started = time.monotonic()
            self.timer_segment_started = self.timer_remaining
            self.tick_timer()

    def persist_timer_segment(self):
        if not self.timer_running or self.timer_started is None:
            return
        elapsed = min(self.timer_segment_started, max(0, int(time.monotonic() - self.timer_started)))
        self.timer_remaining = max(0, self.timer_segment_started - elapsed)
        if self.timer_mode == "focus" and elapsed:
            key = self.today_key()
            self.store.data["work_seconds"][key] = int(self.store.data["work_seconds"].get(key, 0)) + elapsed
        self.timer_started = None
        self.store.save()

    def pause_timer(self):
        self.persist_timer_segment()
        self.timer_running = False
        if self.timer_after:
            self.after_cancel(self.timer_after)
            self.timer_after = None
        self.update_timer()

    def reset_timer(self):
        self.pause_timer()
        self.timer_mode = "focus"
        self.timer_remaining = self.pomodoro_durations()["focus"]
        self.timer_segment_started = self.timer_remaining
        self.update_timer()

    def phase_remaining(self):
        if self.timer_running and self.timer_started is not None:
            elapsed = time.monotonic() - self.timer_started
            return max(0.0, self.timer_segment_started - elapsed)
        return float(self.timer_remaining)

    def current_seconds(self):
        seconds = int(self.store.data["work_seconds"].get(self.today_key(), 0))
        if self.timer_running and self.timer_mode == "focus" and self.timer_started is not None:
            seconds += min(self.timer_segment_started, int(time.monotonic() - self.timer_started))
        return seconds

    def complete_timer_phase(self):
        completed_mode = self.timer_mode
        self.persist_timer_segment()
        self.timer_running = False
        if completed_mode == "focus":
            key = self.today_key()
            sessions = self.today_sessions() + 1
            self.store.data["pomodoro_sessions"][key] = sessions
            self.timer_mode = "long_break" if sessions % 4 == 0 else "short_break"
            self.timer_remaining = self.pomodoro_durations()[self.timer_mode]
            self.timer_segment_started = self.timer_remaining
            self.timer_running = True
            self.timer_started = time.monotonic()
            self.bell()
        else:
            self.timer_mode = "focus"
            self.timer_remaining = self.pomodoro_durations()["focus"]
            self.timer_segment_started = self.timer_remaining
            self.bell()
        self.store.save()
        self.update_timer()

    def update_timer(self):
        seconds = self.current_seconds()
        h, rem = divmod(seconds, 3600)
        m = rem // 60
        target = int(self.store.data.get("daily_target_hours", 6))
        progress = min(100, seconds / (target * 3600) * 100)
        remaining = math.ceil(self.phase_remaining())
        phase_m, phase_s = divmod(remaining, 60)
        phase_name = {"focus": "Фокус", "short_break": "Короткий отдых", "long_break": "Длинный отдых"}[self.timer_mode]
        state = "идёт" if self.timer_running else "готов"
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.configure(text=f"{h} ч {m:02} мин / {target} ч")
        if hasattr(self, "timer_status_label") and self.timer_status_label.winfo_exists():
            self.timer_status_label.configure(text=f"{phase_name} {state} · {phase_m:02}:{phase_s:02}")
        if hasattr(self, "timer_progress") and self.timer_progress.winfo_exists():
            self.timer_progress.configure(value=progress)
        pomodoro = self.windows.get("pomodoro")
        if pomodoro and pomodoro.winfo_exists():
            pomodoro.update_view()

    def tick_timer(self):
        if self.timer_running and self.phase_remaining() <= 0:
            self.complete_timer_phase()
        self.update_timer()
        if self.timer_running:
            self.timer_after = self.after(200, self.tick_timer)

    def destroy(self):
        self.pause_timer()
        super().destroy()


class PomodoroWindow(tk.Toplevel):
    """Спокойный Pomodoro-экран с дневной целью и плавным кольцом прогресса."""

    def __init__(self, master):
        super().__init__(master)
        self.app = master
        self.title("Job Search OS · Рабочий таймер")
        self.geometry("760x760")
        self.minsize(680, 700)
        self.configure(bg=BG)
        self.goal_buttons = {}
        self.preset_buttons = {}
        self.bind("<space>", lambda _event: self.app.toggle_timer())
        self.bind("<Key-r>", lambda _event: self.app.reset_timer())
        self.build()
        self.update_view()

    def build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=38, pady=(30, 12))
        label(header, "POMODORO", size=9, color="#8F82FF", bold=True, pack={"anchor": "w"})
        label(header, "Рабочий ритм", size=27, bold=True, pack={"anchor": "w", "pady": (4, 2)})
        label(header, "Одна сессия за раз. В дневной прогресс идёт только время фокуса.",
              color=MUTED, pack={"anchor": "w"})

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=38, pady=(8, 30))
        left = tk.Frame(body, bg=PANEL, padx=24, pady=22, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(body, bg=PANEL, padx=22, pady=22, width=255,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        self.phase_label = label(left, "ФОКУС", size=9, color=ACCENT, bold=True,
                                 pack={"anchor": "center", "pady": (0, 4)})
        self.canvas = tk.Canvas(left, width=310, height=310, bg=PANEL, highlightthickness=0)
        self.canvas.pack(pady=(0, 8))
        self.canvas.create_oval(28, 28, 282, 282, outline="#24314D", width=14, tags="track")
        self.canvas.create_arc(28, 28, 282, 282, start=90, extent=0, style="arc",
                               outline=ACCENT, width=14, tags="progress")
        self.canvas.create_oval(146, 21, 164, 39, fill=ACCENT, outline="", tags="pulse")
        self.canvas.create_text(155, 142, text="50:00", fill=TEXT,
                                font=(FONT, 38, "bold"), tags="countdown")
        self.canvas.create_text(155, 188, text="сессия готова", fill=MUTED,
                                font=(FONT, 10), tags="state")

        actions = tk.Frame(left, bg=PANEL)
        actions.pack(pady=(2, 14))
        self.start_button = button(actions, "Начать фокус", self.app.toggle_timer, primary=True, width=15)
        self.start_button.pack(side="left", padx=(0, 8))
        button(actions, "Сбросить сессию", self.app.reset_timer, width=15).pack(side="left")

        label(left, "ДЛИТЕЛЬНОСТЬ", size=8, color=MUTED, bold=True,
              pack={"anchor": "center", "pady": (7, 7)})
        presets = tk.Frame(left, bg=PANEL)
        presets.pack()
        for preset in ("50/10", "25/5"):
            control = button(presets, preset, lambda value=preset: self.app.set_pomodoro_preset(value), width=9)
            control.pack(side="left", padx=4)
            self.preset_buttons[preset] = control

        label(right, "СЕГОДНЯ", size=8, color="#8F82FF", bold=True, pack={"anchor": "w"})
        self.daily_label = label(right, "0 ч 00 мин", size=22, bold=True,
                                 pack={"anchor": "w", "pady": (5, 2)})
        self.goal_text = label(right, "до цели осталось 6 ч", size=9, color=MUTED,
                               pack={"anchor": "w", "pady": (0, 12)})
        self.daily_progress = ttk.Progressbar(right, maximum=100, value=0,
                                              style="Focus.Horizontal.TProgressbar")
        self.daily_progress.pack(fill="x", pady=(0, 18))

        label(right, "ДНЕВНАЯ ЦЕЛЬ", size=8, color=MUTED, bold=True,
              pack={"anchor": "w", "pady": (0, 7)})
        goals = tk.Frame(right, bg=PANEL)
        goals.pack(fill="x", pady=(0, 18))
        for hours in (4, 6, 8, 9):
            control = button(goals, f"{hours} ч", lambda value=hours: self.app.set_daily_target(value), width=4)
            control.pack(side="left", padx=(0, 5))
            self.goal_buttons[hours] = control

        label(right, "ЗАВЕРШЁННЫЕ СЕССИИ", size=8, color=MUTED, bold=True,
              pack={"anchor": "w", "pady": (0, 8)})
        self.sessions_label = label(right, "○ ○ ○ ○", size=18, color=MUTED,
                                    pack={"anchor": "w", "pady": (0, 6)})
        self.sessions_text = label(right, "0 сессий", size=9, color=MUTED,
                                   pack={"anchor": "w", "pady": (0, 18)})

        tip = tk.Frame(right, bg="#18233D", padx=13, pady=12)
        tip.pack(fill="x", side="bottom")
        label(tip, "После 4 сессий", size=9, bold=True, bg="#18233D", pack={"anchor": "w"})
        self.long_break_tip = label(tip, "Автоматически начнётся длинный перерыв.", size=9,
                                    color=MUTED, bg="#18233D", wrap=195,
                                    pack={"anchor": "w", "pady": (3, 0)})

    def update_view(self):
        remaining = max(0, math.ceil(self.app.phase_remaining()))
        minutes, seconds = divmod(remaining, 60)
        durations = self.app.pomodoro_durations()
        duration = durations[self.app.timer_mode]
        progress = 1 - min(1, remaining / max(1, duration))
        color = ACCENT if self.app.timer_mode == "focus" else SUCCESS
        phase = {"focus": "ФОКУС", "short_break": "КОРОТКИЙ ОТДЫХ", "long_break": "ДЛИННЫЙ ОТДЫХ"}[self.app.timer_mode]
        state = "сессия идёт" if self.app.timer_running else "сессия готова"
        pulse = 3 * math.sin(time.monotonic() * 4) if self.app.timer_running else 0
        self.phase_label.configure(text=phase, fg=color)
        self.canvas.itemconfigure("countdown", text=f"{minutes:02}:{seconds:02}")
        self.canvas.itemconfigure("state", text=state)
        self.canvas.itemconfigure("progress", extent=-359.9 * progress, outline=color)
        self.canvas.coords("pulse", 146 - pulse, 21 - pulse, 164 + pulse, 39 + pulse)
        self.canvas.itemconfigure("pulse", fill=color)
        self.start_button.configure(text="Пауза" if self.app.timer_running else (
            "Начать фокус" if self.app.timer_mode == "focus" else "Начать отдых"
        ))

        focus = self.app.current_seconds()
        hours, rest = divmod(focus, 3600)
        mins = rest // 60
        target = int(self.app.store.data.get("daily_target_hours", 6))
        left = max(0, target * 3600 - focus)
        left_h, left_rest = divmod(left, 3600)
        left_m = math.ceil(left_rest / 60)
        self.daily_label.configure(text=f"{hours} ч {mins:02} мин")
        self.goal_text.configure(
            text="Дневная цель выполнена" if left == 0 else f"до цели осталось {left_h} ч {left_m:02} мин",
            fg=SUCCESS if left == 0 else MUTED,
        )
        self.daily_progress.configure(value=min(100, focus / (target * 3600) * 100))

        sessions = self.app.today_sessions()
        cycle = sessions % 4
        self.sessions_label.configure(text=" ".join("●" if index < cycle else "○" for index in range(4)),
                                      fg=SUCCESS if cycle else MUTED)
        self.sessions_text.configure(text=f"{sessions} сессий · {sessions // 4} полных циклов")

        selected_goal = int(self.app.store.data.get("daily_target_hours", 6))
        for value, control in self.goal_buttons.items():
            control.configure(bg=ACCENT if value == selected_goal else PANEL_2)
        selected_preset = self.app.store.data.get("pomodoro_preset", "50/10")
        for value, control in self.preset_buttons.items():
            control.configure(bg=ACCENT if value == selected_preset else PANEL_2)
        self.long_break_tip.configure(
            text=f"Автоматически начнётся длинный перерыв на {durations['long_break'] // 60} минут."
        )


class TodayWindow(tk.Toplevel):
    """Календарный экран дня: план не подменяется первым незавершённым днём."""

    def __init__(self, master, store, open_track, open_pomodoro):
        super().__init__(master)
        self.store = store
        self.open_track = open_track
        self.open_pomodoro = open_pomodoro
        self.title("Job Search OS · Сегодня")
        self.geometry("1050x820")
        self.minsize(860, 680)
        self.configure(bg=BG)
        self.render()

    def render(self):
        for widget in self.winfo_children():
            widget.destroy()
        today = datetime.now().date()
        day, upcoming = calendar_day(today)
        debts = overdue_tasks(self.store, today)

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=32, pady=(26, 16))
        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left", fill="x", expand=True)
        label(title_box, "СЕГОДНЯ", size=9, color=ACCENT, bold=True, pack={"anchor": "w"})
        label(title_box, today.strftime("%d.%m.%Y"), size=27, bold=True,
              pack={"anchor": "w", "pady": (3, 2)})
        subtitle = "Следуй темам текущей даты. Незавершённые прошлые темы показаны отдельно."
        label(title_box, subtitle, color=MUTED, pack={"anchor": "w"})
        button(header, "Pomodoro", self.open_pomodoro, primary=True).pack(side="right")

        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        parent = scroll.inner

        if day:
            done = sum(self.store.solved(task_id) for task_id in day["task_ids"])
            hours, minutes = divmod(day["minutes"], 60)
            summary = tk.Frame(parent, bg="#182441", padx=20, pady=16,
                               highlightbackground=ACCENT, highlightthickness=1)
            summary.pack(fill="x", padx=5, pady=(0, 12))
            label(summary, f'День {day["number"]} · {done}/{len(day["task_ids"])} задач',
                  size=15, bold=True, bg="#182441", pack={"side": "left"})
            label(summary, f"Плановая нагрузка: {hours} ч {minutes:02} мин", color=MUTED,
                  bg="#182441", pack={"side": "right"})
            phase = tk.Frame(parent, bg=PANEL, padx=20, pady=14,
                             highlightbackground=BORDER, highlightthickness=1)
            phase.pack(fill="x", padx=5, pady=(0, 12))
            label(phase, day["phase"]["title"].upper(), size=9, color=ACCENT, bold=True,
                  pack={"anchor": "w"})
            label(phase, day["phase"]["goal"], color=MUTED, wrap=850,
                  pack={"anchor": "w", "pady": (5, 2)})
            label(phase, f'Контрольная точка: {day["phase"]["milestone"]}', color=TEXT, wrap=850,
                  pack={"anchor": "w", "pady": (4, 0)})
            label(phase, f'Повторение и проверка: {day["review_minutes"]} минут.', color=SUCCESS,
                  pack={"anchor": "w", "pady": (4, 0)})
            breakdown = (
                f'Обучение {day["learning_minutes"]} мин · проверка навыков {day["verification_minutes"]} мин · '
                f'закрепление {day["consolidation_minutes"]} мин · HH-разминка {day["career_minutes"]} мин'
            )
            label(phase, breakdown, color=BLUE, wrap=850,
                  pack={"anchor": "w", "pady": (4, 0)})
            for track, topic in day["topics"]:
                self.topic_card(parent, track, topic)
            self.review_card(parent, day, debts)
            self.career_action_card(parent, day)
        else:
            rest = tk.Frame(parent, bg=PANEL, padx=22, pady=20,
                            highlightbackground=BORDER, highlightthickness=1)
            rest.pack(fill="x", padx=5, pady=(0, 12))
            label(rest, "Новых тем на сегодня нет", size=16, bold=True, pack={"anchor": "w"})
            message = (f'Следующий учебный день — {upcoming["date"].strftime("%d.%m.%Y")}.'
                       if upcoming else "Основной учебный план завершён.")
            label(rest, message + " Можно закрыть накопившиеся темы или пройти пробное собеседование.",
                  color=MUTED, wrap=850, pack={"anchor": "w", "pady": (5, 0)})

        debt_tasks = sum(len(item["tasks"]) for item in debts)
        debt_box = tk.Frame(parent, bg=PANEL, padx=20, pady=17,
                            highlightbackground=BORDER, highlightthickness=1)
        debt_box.pack(fill="x", padx=5, pady=(8, 8))
        label(debt_box, "НЕЗАВЕРШЁННОЕ ИЗ ПРОШЛЫХ ДНЕЙ", size=9,
              color=WARNING if debt_tasks else SUCCESS, bold=True, pack={"anchor": "w"})
        if not debts:
            label(debt_box, "Долгов нет — план выполняется по календарю.", color=SUCCESS,
                  pack={"anchor": "w", "pady": (7, 0)})
        else:
            label(debt_box, f"{len(debts)} тем · {debt_tasks} задач. Начни с самой ранней темы.",
                  color=MUTED, pack={"anchor": "w", "pady": (5, 8)})
            for item in debts[:6]:
                row = tk.Frame(debt_box, bg=PANEL)
                row.pack(fill="x", pady=4)
                label(row, f'{item["day"]["date"].strftime("%d.%m")} · {item["track"]["title"]} · {item["topic"]["title"]}',
                      pack={"side": "left"})
                button(row, "Продолжить", lambda it=item: self.open_track(it["track"], it["topic"]["id"]),
                       width=10).pack(side="right")
            if len(debts) > 6:
                label(debt_box, f"Ещё {len(debts) - 6} тем видны в общем плане.", color=MUTED,
                      pack={"anchor": "w", "pady": (6, 0)})

    def topic_card(self, parent, track, topic):
        tasks = topic["tasks"]
        done = sum(self.store.solved(task["id"]) for task in tasks)
        card = tk.Frame(parent, bg=PANEL, padx=20, pady=16,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=5, pady=6)
        top = tk.Frame(card, bg=PANEL)
        top.pack(fill="x")
        label(top, f'{track["title"]} · {topic["title"]}', size=13, bold=True,
              pack={"side": "left"})
        button(top, "Открыть тему →", lambda: self.open_track(track, topic["id"]),
               primary=done < len(tasks)).pack(side="right")
        label(card, f"{done}/{len(tasks)} заданий", color=SUCCESS if done == len(tasks) else MUTED,
              pack={"anchor": "w", "pady": (4, 8)})
        for task in tasks:
            solved = self.store.solved(task["id"])
            label(card, f'{"✓" if solved else "○"}  {task["title"]}',
                  color=SUCCESS if solved else TEXT, wrap=800,
                  pack={"anchor": "w", "pady": 2})

    def review_card(self, parent, day, debts):
        reviews = [
            (track, topic) for track, topic in day.get("review_topics", [])
            if all(self.store.solved(task["id"]) for task in topic["tasks"])
        ]
        box = tk.Frame(parent, bg="#152C2B", padx=20, pady=16,
                       highlightbackground="#28665C", highlightthickness=1)
        box.pack(fill="x", padx=5, pady=(12, 6))
        quest = day["quest"]
        done = quest["key"] in self.store.data.get("daily_quests", {})
        label(box, f'ПРАКТИЧЕСКАЯ ПРОВЕРКА · {quest["minutes"]} МИНУТ', size=9, color=SUCCESS, bold=True,
              bg="#152C2B", pack={"anchor": "w"})
        label(box, f'{"✓ " if done else ""}{quest["title"]}', size=14, color=SUCCESS if done else TEXT,
              bold=True, bg="#152C2B", pack={"anchor": "w", "pady": (5, 2)})
        label(box, quest["description"], color=MUTED, bg="#152C2B", wrap=850,
              pack={"anchor": "w", "pady": (0, 9)})
        actions = tk.Frame(box, bg="#152C2B")
        actions.pack(fill="x", pady=(0, 10))
        button(actions, "Скопировать квест", lambda: self.copy_daily_quest(quest), primary=not done).pack(side="left")
        if not done:
            button(actions, "Квест выполнен +100 XP",
                   lambda: self.finish_daily_quest(quest["key"])).pack(side="right")
        else:
            label(actions, "Получено 100 XP", color=SUCCESS, bold=True, bg="#152C2B", pack={"side": "right"})

        label(box, "ТЕМЫ ДЛЯ ВОСПРОИЗВЕДЕНИЯ ИЗ ПАМЯТИ", size=8, color=MUTED, bold=True,
              bg="#152C2B", pack={"anchor": "w", "pady": (4, 2)})
        if not reviews:
            message = ("Сначала закрой самую раннюю незавершённую тему — сегодня она заменяет повторение."
                       if debts else "В первые дни отдельные темы для интервального повторения ещё не накопились.")
            label(box, message, color=MUTED, bg="#152C2B", wrap=850,
                  pack={"anchor": "w", "pady": (6, 0)})
            return
        label(box, "Без конспекта объясни главное, назови типичную ошибку и восстанови решение или пример.",
              color=MUTED, bg="#152C2B", wrap=850, pack={"anchor": "w", "pady": (5, 8)})
        for track, topic in reviews:
            row = tk.Frame(box, bg="#152C2B")
            row.pack(fill="x", pady=3)
            label(row, f'{track["title"]} · {topic["title"]}', bg="#152C2B", pack={"side": "left"})
            button(row, "Открыть", lambda tr=track, tp=topic: self.open_track(tr, tp["id"]), width=9).pack(side="right")

    def copy_daily_quest(self, quest):
        self.clipboard_clear()
        self.clipboard_append(quest["prompt"])
        self.update()
        messagebox.showinfo("Квест скопирован", "Открой новый чат с AI-наставником и начни квест.", parent=self)

    def finish_daily_quest(self, quest_key):
        self.store.complete_quest(quest_key)
        self.render()

    def career_action_card(self, parent, day):
        action = day["career_action"]
        done = action["key"] in self.store.data.get("career_actions", {})
        minutes = day["career_minutes"]
        box = tk.Frame(parent, bg="#111F38", padx=20, pady=16,
                       highlightbackground=BLUE, highlightthickness=1)
        box.pack(fill="x", padx=5, pady=(8, 6))
        label(box, f'HH-РАЗМИНКА · {minutes} МИНУТ', size=9, color=BLUE, bold=True,
              bg="#111F38", pack={"anchor": "w"})
        label(box, f'{"✓ " if done else ""}{action["title"]}', size=14,
              color=SUCCESS if done else TEXT, bold=True, bg="#111F38",
              pack={"anchor": "w", "pady": (5, 2)})
        label(box, action["description"], color=MUTED, bg="#111F38", wrap=850,
              pack={"anchor": "w", "pady": (0, 8)})
        if not done:
            button(box, "Разминка выполнена", lambda: self.finish_career_action(action["key"]),
                   primary=True).pack(anchor="e")

    def finish_career_action(self, action_key):
        self.store.complete_career_action(action_key)
        self.render()


class SkillMatrixWindow(tk.Toplevel):
    def __init__(self, master, store, open_track, on_change):
        super().__init__(master)
        self.store = store
        self.open_track = open_track
        self.on_change = on_change
        self.track = sorted(CURRICULUM, key=lambda item: CAREER_TRACK_ORDER[item["id"]])[0]
        self.title("Job Search OS · Матрица навыков")
        self.geometry("1180x840")
        self.minsize(960, 700)
        self.configure(bg=BG)
        self.render()

    def select_track(self, track):
        self.track = track
        self.render()

    def render(self):
        for widget in self.winfo_children():
            widget.destroy()
        metrics = readiness_summary(self.store)
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 14))
        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left", fill="x", expand=True)
        label(title_box, "МАТРИЦА НАВЫКОВ", size=9, color=ACCENT, bold=True,
              pack={"anchor": "w"})
        label(title_box, "Решил — значит завершил", size=25, bold=True,
              pack={"anchor": "w", "pady": (3, 2)})
        label(title_box, "Матрица показывает завершённые темы без дополнительного статуса подтверждения.",
              color=MUTED, pack={"anchor": "w"})
        label(header, f'{metrics["studied"]}/{metrics["total_topics"]}', size=26, color=ACCENT, bold=True,
              pack={"side": "right"})

        tabs = tk.Frame(self, bg=BG)
        tabs.pack(fill="x", padx=30, pady=(0, 12))
        ordered = sorted(CURRICULUM, key=lambda item: CAREER_TRACK_ORDER[item["id"]])
        for track in ordered:
            control = button(tabs, track["icon"], lambda item=track: self.select_track(item),
                             primary=track["id"] == self.track["id"], width=4)
            control.pack(side="left", padx=(0, 5))

        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        parent = scroll.inner
        label(parent, self.track["title"], size=20, bold=True, pack={"anchor": "w", "padx": 5, "pady": (0, 8)})
        for topic in self.track["topics"]:
            studied = topic_studied(self.store, topic)
            card = tk.Frame(parent, bg=PANEL, padx=16, pady=12,
                            highlightbackground=SUCCESS if studied else BORDER, highlightthickness=1)
            card.pack(fill="x", padx=5, pady=4)
            status = "ЗАВЕРШЕНО" if studied else "В РАБОТЕ"
            status_color = SUCCESS if studied else MUTED
            label(card, f'{topic["number"]:02}. {topic["title"]}', size=11, bold=True,
                  pack={"side": "left"})
            actions = tk.Frame(card, bg=PANEL)
            actions.pack(side="right")
            label(actions, status, size=8, color=status_color, bold=True,
                  pack={"side": "left", "padx": 8})
            button(actions, "Тема", lambda tp=topic: self.open_track(self.track, tp["id"]), width=7).pack(side="left", padx=3)


class ProjectProofWindow(tk.Toplevel):
    def __init__(self, master, store, on_change):
        super().__init__(master)
        self.store = store
        self.on_change = on_change
        self.title("Job Search OS · Проектные доказательства")
        self.geometry("1080x820")
        self.minsize(880, 680)
        self.configure(bg=BG)
        self.render()

    def render(self):
        for widget in self.winfo_children():
            widget.destroy()
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 14))
        label(header, "ПРОЕКТНЫЕ ДОКАЗАТЕЛЬСТВА", size=9, color=BLUE, bold=True, pack={"anchor": "w"})
        label(header, "Код сам по себе ничего не доказывает", size=25, bold=True,
              pack={"anchor": "w", "pady": (3, 2)})
        label(header, "Каждый milestone требует воспроизводимого артефакта и способности защитить решение на интервью.",
              color=MUTED, pack={"anchor": "w"})
        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=25, pady=(0, 24))
        parent = scroll.inner
        records = self.store.data.get("project_records", {})
        for project in PROJECTS:
            card = tk.Frame(parent, bg=PANEL, padx=20, pady=16, highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", padx=5, pady=7)
            completed = records.get(project["id"], {})
            count = sum(bool(completed.get(item_id, {}).get("evidence")) for item_id, _title, _desc in project["milestones"])
            label(card, project["title"], size=16, bold=True, pack={"anchor": "w"})
            label(card, f'{count}/{len(project["milestones"])} доказательств · {project["description"]}',
                  color=MUTED, wrap=930, pack={"anchor": "w", "pady": (4, 10)})
            for item_id, title, description in project["milestones"]:
                done = bool(completed.get(item_id, {}).get("evidence"))
                row = tk.Frame(card, bg=PANEL_2, padx=12, pady=10)
                row.pack(fill="x", pady=3)
                info = tk.Frame(row, bg=PANEL_2)
                info.pack(side="left", fill="x", expand=True)
                label(info, f'{"✓ " if done else "○ "}{title}', color=SUCCESS if done else TEXT,
                      bold=True, bg=PANEL_2, pack={"anchor": "w"})
                label(info, description, size=9, color=MUTED, bg=PANEL_2, wrap=760,
                      pack={"anchor": "w", "pady": (3, 0)})
                button(row, "Доказательство", lambda p=project, mid=item_id, t=title: self.open_evidence(p, mid, t),
                       primary=not done).pack(side="right", padx=(10, 0))

    def open_evidence(self, project, milestone_id, title):
        EvidenceWindow(self, self.store, project["id"], milestone_id, title, self.after_save)

    def after_save(self):
        self.render()
        self.on_change()


class EvidenceWindow(tk.Toplevel):
    def __init__(self, master, store, project_id, milestone_id, title, on_saved):
        super().__init__(master)
        self.store = store
        self.project_id = project_id
        self.milestone_id = milestone_id
        self.on_saved = on_saved
        self.title(f"Доказательство · {title}")
        self.geometry("680x420")
        self.configure(bg=BG)
        record = store.data.get("project_records", {}).get(project_id, {}).get(milestone_id, {})
        label(self, title, size=19, bold=True, pack={"anchor": "w", "padx": 24, "pady": (22, 4)})
        label(self, "Ссылка, путь, команда проверки и краткое объяснение того, что именно доказано.",
              color=MUTED, wrap=620, pack={"anchor": "w", "padx": 24, "pady": (0, 10)})
        self.text = tk.Text(self, bg="#091626", fg=TEXT, insertbackground=TEXT, relief="flat",
                            wrap="word", padx=12, pady=10)
        self.text.insert("1.0", record.get("evidence", ""))
        self.text.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        button(self, "Сохранить доказательство", self.save, primary=True).pack(anchor="e", padx=24, pady=(0, 20))

    def save(self):
        evidence = self.text.get("1.0", "end").strip()
        if len(evidence) < 30:
            messagebox.showerror("Недостаточно", "Доказательство должно быть конкретным и проверяемым.", parent=self)
            return
        self.store.save_project_evidence(self.project_id, self.milestone_id, evidence)
        self.on_saved()
        self.destroy()


class ResumeLabWindow(tk.Toplevel):
    def __init__(self, master, store, on_change):
        super().__init__(master)
        self.store = store
        self.on_change = on_change
        self.title("Job Search OS · Резюме")
        self.geometry("1050x820")
        self.minsize(860, 680)
        self.configure(bg=BG)
        self.render()

    def render(self):
        for widget in self.winfo_children():
            widget.destroy()
        profile = self.store.data.get("career_profile", {})
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 14))
        label(header, "РЕЗЮМЕ И ПОЗИЦИОНИРОВАНИЕ", size=9, color=WARNING, bold=True, pack={"anchor": "w"})
        label(header, "Не обещания, а проверяемые факты", size=25, bold=True, pack={"anchor": "w", "pady": (3, 2)})
        label(header, "В резюме попадает только то, что можно защитить кодом, артефактом или отдельной проверкой.",
              color=MUTED, pack={"anchor": "w"})
        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=25, pady=(0, 24))
        parent = scroll.inner

        fields = tk.Frame(parent, bg=PANEL, padx=18, pady=16, highlightbackground=BORDER, highlightthickness=1)
        fields.pack(fill="x", padx=5, pady=5)
        self.entries = {}
        for key, title, default in (
            ("headline", "Заголовок", "Junior Python Backend Developer · Django · PostgreSQL"),
            ("salary", "Минимально приемлемая зарплата", ""),
            ("location", "Город и форматы работы", ""),
        ):
            label(fields, title, color=MUTED, pack={"anchor": "w", "pady": (6, 3)})
            entry = tk.Entry(fields, bg="#091626", fg=TEXT, insertbackground=TEXT, relief="flat", font=(FONT, 10))
            entry.insert(0, profile.get(key, default))
            entry.pack(fill="x", ipady=7)
            self.entries[key] = entry
        label(fields, "Рассказ о себе на 60–90 секунд", color=MUTED, pack={"anchor": "w", "pady": (10, 3)})
        self.pitch = tk.Text(fields, height=5, bg="#091626", fg=TEXT, insertbackground=TEXT,
                             relief="flat", wrap="word", padx=10, pady=8)
        self.pitch.insert("1.0", profile.get("pitch", ""))
        self.pitch.pack(fill="x")
        label(fields, "Текст резюме", color=MUTED, pack={"anchor": "w", "pady": (10, 3)})
        self.resume_text = tk.Text(fields, height=12, bg="#091626", fg=TEXT, insertbackground=TEXT,
                                   relief="flat", wrap="word", padx=10, pady=8)
        self.resume_text.insert("1.0", profile.get("resume_text", ""))
        self.resume_text.pack(fill="x")

        checklist = tk.Frame(parent, bg=PANEL, padx=18, pady=16, highlightbackground=BORDER, highlightthickness=1)
        checklist.pack(fill="x", padx=5, pady=8)
        label(checklist, "ЧЕК-ЛИСТ ДОПУСКА К ОТКЛИКАМ", size=9, color=ACCENT, bold=True,
              pack={"anchor": "w", "pady": (0, 7)})
        self.check_vars = {}
        for key, text_value in RESUME_CHECKLIST:
            var = tk.BooleanVar(value=bool(self.store.data.get("resume_checklist", {}).get(key)))
            self.check_vars[key] = var
            tk.Checkbutton(checklist, text=text_value, variable=var, bg=PANEL, fg=TEXT,
                           selectcolor=PANEL_2, activebackground=PANEL, activeforeground=TEXT,
                           anchor="w", justify="left", wraplength=900).pack(fill="x", pady=3)
        actions = tk.Frame(parent, bg=BG)
        actions.pack(fill="x", padx=5, pady=8)
        button(actions, "Скопировать промпт аудита", self.copy_audit_prompt).pack(side="left")
        button(actions, "Сохранить", self.save, primary=True).pack(side="right")

    def audit_prompt(self):
        return f"""Ты — строгий рекрутер и hiring manager на Junior Python Backend Developer. Проведи аудит резюме, не переписывая опыт и не добавляя навыки, которых нет.

Целевая роль: {self.entries['headline'].get().strip()}
Рассказ о себе:
{self.pitch.get('1.0', 'end').strip()}

Резюме:
{self.resume_text.get('1.0', 'end').strip()}

Проверь: соответствие вакансии; первые 15 секунд просмотра; конкретность результатов; доказуемость каждого технического тезиса; ключевые слова Python/Django/DRF/PostgreSQL/SQL/Linux/Docker/Git/HTTP/tests; отсутствие преувеличений; качество описания EidosAcademy; причины возможного отказа.

Верни: 1) стоп-факторы; 2) недоказанные заявления; 3) что убрать; 4) что уточнить цифрой или ссылкой; 5) улучшенную структуру без выдуманных фактов; 6) десять вопросов, которыми интервьюер проверит самые сильные заявления. Вопросы должны проверять разные навыки и не повторяться по смыслу."""

    def copy_audit_prompt(self):
        self.clipboard_clear()
        self.clipboard_append(self.audit_prompt())
        self.update()
        messagebox.showinfo("Готово", "Промпт аудита резюме скопирован.", parent=self)

    def save(self):
        self.store.data["career_profile"] = {
            **self.store.data.get("career_profile", {}),
            **{key: entry.get().strip() for key, entry in self.entries.items()},
            "pitch": self.pitch.get("1.0", "end").strip(),
            "resume_text": self.resume_text.get("1.0", "end").strip(),
            "updated_at": datetime.now().isoformat(timespec="minutes"),
        }
        self.store.data["resume_checklist"] = {key: var.get() for key, var in self.check_vars.items()}
        self.store.save()
        self.on_change()
        messagebox.showinfo("Сохранено", "Профиль и чек-лист обновлены.", parent=self)




class WeeklyReportWindow(tk.Toplevel):
    def __init__(self, master, store):
        super().__init__(master)
        self.store = store
        self.anchor = datetime.now().date()
        self.title("Job Search OS · Недельный отчёт")
        self.geometry("980x800")
        self.minsize(820, 660)
        self.configure(bg=BG)
        self.render()

    def move_week(self, offset):
        self.anchor += timedelta(days=7 * offset)
        self.render()

    def render(self):
        for widget in self.winfo_children():
            widget.destroy()
        report = weekly_summary(self.store, self.anchor)
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=32, pady=(26, 14))
        titles = tk.Frame(header, bg=BG)
        titles.pack(side="left", fill="x", expand=True)
        label(titles, "НЕДЕЛЬНЫЙ ОТЧЁТ", size=9, color=ACCENT, bold=True, pack={"anchor": "w"})
        label(titles, f'{report["start"].strftime("%d.%m")} — {report["end"].strftime("%d.%m.%Y")}',
              size=25, bold=True, pack={"anchor": "w", "pady": (3, 0)})
        controls = tk.Frame(header, bg=BG)
        controls.pack(side="right")
        button(controls, "←", lambda: self.move_week(-1), width=3).pack(side="left", padx=3)
        button(controls, "Эта неделя", self.current_week).pack(side="left", padx=3)
        button(controls, "→", lambda: self.move_week(1), width=3).pack(side="left", padx=3)

        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        parent = scroll.inner
        metrics = tk.Frame(parent, bg=BG)
        metrics.pack(fill="x", padx=2, pady=(0, 12))
        focus_h = report["focus_seconds"] / 3600
        values = [
            (f'{report["completed_planned"]}/{report["planned"]}', "задач к этой дате"),
            (f'{report["percent"]}%', "выполнено к сроку"),
            (str(report["completed_this_week"]), "задач закрыто за неделю"),
            (str(report["applications_this_week"]), "откликов отправлено"),
            (f"{focus_h:.1f} ч", "чистого фокуса"),
        ]
        for index, (value, caption) in enumerate(values):
            metrics.grid_columnconfigure(index, weight=1, uniform="metrics")
            card = tk.Frame(metrics, bg=PANEL, padx=14, pady=14,
                            highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=index, sticky="nsew", padx=4)
            label(card, value, size=19, bold=True, pack={"anchor": "w"})
            label(card, caption, size=9, color=MUTED, pack={"anchor": "w", "pady": (3, 0)})

        plan_box = tk.Frame(parent, bg=PANEL, padx=20, pady=17,
                            highlightbackground=BORDER, highlightthickness=1)
        plan_box.pack(fill="x", padx=5, pady=6)
        label(plan_box, "ВЫПОЛНЕНИЕ ПО НАПРАВЛЕНИЯМ", size=9, color=ACCENT, bold=True,
              pack={"anchor": "w", "pady": (0, 8)})
        if report["by_track"]:
            for item in report["by_track"]:
                row = tk.Frame(plan_box, bg=PANEL)
                row.pack(fill="x", pady=4)
                label(row, item["track"]["title"], pack={"side": "left"})
                color = SUCCESS if item["completed"] == item["planned"] else MUTED
                label(row, f'{item["completed"]}/{item["planned"]}', color=color, bold=True,
                      pack={"side": "right"})
        else:
            label(plan_box, "На этой неделе в календаре нет учебных дней.", color=MUTED,
                  pack={"anchor": "w"})

        facts = tk.Frame(parent, bg=PANEL, padx=20, pady=17,
                         highlightbackground=BORDER, highlightthickness=1)
        facts.pack(fill="x", padx=5, pady=6)
        label(facts, "ФАКТЫ НЕДЕЛИ", size=9, color=ACCENT, bold=True,
              pack={"anchor": "w", "pady": (0, 8)})
        label(facts, f'Закрыто задач в течение недели: {report["completed_this_week"]}',
              pack={"anchor": "w", "pady": 2})
        label(facts, f'Полный план недели: {report["week_planned"]} задач',
              pack={"anchor": "w", "pady": 2})
        label(facts, f'Всего зафиксировано попыток: {report["attempts"]}',
              pack={"anchor": "w", "pady": 2})
        label(facts, f'Коротких HH-разминок: {report["career_actions"]}',
              pack={"anchor": "w", "pady": 2})
        recommendation = self.recommendation(report)
        label(facts, recommendation, color=MUTED, wrap=850,
              pack={"anchor": "w", "pady": (8, 0)})
        button(parent, "Скопировать отчёт", lambda: self.copy_report(report), primary=True).pack(anchor="e", padx=5, pady=10)

    def current_week(self):
        self.anchor = datetime.now().date()
        self.render()

    @staticmethod
    def recommendation(report):
        if not report["planned"]:
            return "Неделя свободна от новых тем. Используй её для повторения и пробного собеседования."
        if report["percent"] >= 90:
            return "Темп устойчивый. Продолжай следующий блок по плану и используй закрепление для воспроизведения без подсказок."
        if report["percent"] >= 60:
            return "План выполнен частично. Сначала закрой ранние незавершённые темы, затем переходи к новым."
        return "Нагрузка отстаёт от плана. Не расширяй список тем: выбери одну незавершённую тему и доведи её до конца."

    def copy_report(self, report):
        focus_h = report["focus_seconds"] / 3600
        lines = [
            f'Недельный отчёт: {report["start"].strftime("%d.%m.%Y")}–{report["end"].strftime("%d.%m.%Y")}',
            f'План: {report["completed_planned"]}/{report["planned"]} задач ({report["percent"]}%)',
            f'Всего назначено на неделю: {report["week_planned"]}',
            f'Закрыто за неделю: {report["completed_this_week"]}; попыток: {report["attempts"]}',
            f'Откликов отправлено: {report["applications_this_week"]}',
            f'Фокус: {focus_h:.1f} ч; Pomodoro: {report["sessions"]}; активных дней: {report["active_days"]}/7',
            self.recommendation(report),
        ]
        self.clipboard_clear()
        self.clipboard_append("\n".join(lines))
        self.update()
        messagebox.showinfo("Готово", "Недельный отчёт скопирован.", parent=self)




class PlanWindow(tk.Toplevel):
    def __init__(self, master, store, open_track):
        super().__init__(master)
        self.store = store
        self.open_track = open_track
        self.title("Job Search OS · План по дням")
        self.geometry("1080x820")
        self.minsize(900, 680)
        self.configure(bg=BG)
        self.render()

    def render(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 16))
        label(header, "План по дням", size=24, bold=True, pack={"anchor": "w"})
        label(header, f"{len(build_daily_plan())} учебных дней · рабочий режим 9 часов · воскресенье без новых тем",
              color=MUTED, pack={"anchor": "w", "pady": (4, 0)})
        scroll = ScrollFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        for checkpoint, requirement in CHECKPOINTS:
            label(scroll.inner, f"{checkpoint} · {requirement}", wrap=950, color=WARNING,
                  pack={"anchor": "w", "padx": 8, "pady": 4})
        today = datetime.now().date()
        previous_phase = None
        for day in build_daily_plan():
            if day["phase"]["id"] != previous_phase:
                self.phase_header(scroll.inner, day["phase"])
                previous_phase = day["phase"]["id"]
            self.day_card(scroll.inner, day, today)

    def phase_header(self, parent, phase):
        box = tk.Frame(parent, bg="#182441", padx=20, pady=16,
                       highlightbackground=ACCENT, highlightthickness=1)
        box.pack(fill="x", padx=5, pady=(16, 8))
        label(box, phase["title"], size=16, color=TEXT, bold=True, bg="#182441",
              pack={"anchor": "w"})
        label(box, phase["goal"], color=MUTED, bg="#182441", wrap=950,
              pack={"anchor": "w", "pady": (5, 2)})
        label(box, f'Контрольная точка: {phase["milestone"]}', color=SUCCESS, bg="#182441", wrap=950,
              pack={"anchor": "w", "pady": (5, 0)})

    def day_card(self, parent, day, today):
        active = day["date"] == today
        done = sum(self.store.solved(task_id) for task_id in day["task_ids"])
        card = tk.Frame(parent, bg="#182441" if active else PANEL, padx=18, pady=15,
                        highlightbackground="#7C6CFF" if active else BORDER, highlightthickness=1)
        card.pack(fill="x", padx=5, pady=6)
        top = tk.Frame(card, bg=card.cget("bg"))
        top.pack(fill="x")
        label(top, f'День {day["number"]:03} · {day["date"].strftime("%d.%m.%Y")}',
              size=11, bold=True, bg=card.cget("bg"), pack={"side": "left"})
        label(top, f'{done}/{len(day["task_ids"])} задач' if day["task_ids"] else 'Интервью / разбор ошибок', color=SUCCESS if day["task_ids"] and done == len(day["task_ids"]) else MUTED,
              bold=True, bg=card.cget("bg"), pack={"side": "right"})
        label(card, day["phase"]["title"], size=9, color=ACCENT, bold=True,
              bg=card.cget("bg"), pack={"anchor": "w", "pady": (6, 0)})
        label(card, f'Обучение {day["learning_minutes"]} мин · проверка {day["verification_minutes"]} мин · закрепление {day["consolidation_minutes"]} мин · HH {day["career_minutes"]} мин',
              size=9, color=BLUE, bg=card.cget("bg"), pack={"anchor": "w", "pady": (3, 0)})
        for track, topic in day["topics"]:
            row = tk.Frame(card, bg=card.cget("bg"))
            row.pack(fill="x", pady=(10, 0))
            topic_done = sum(self.store.solved(task["id"]) for task in topic["tasks"])
            label(row, f'{track["title"]}  ·  {topic["title"]}  ·  {topic_done}/{len(topic["tasks"])}',
                  size=10, bg=card.cget("bg"), pack={"side": "left"})
            button(row, "Открыть", lambda tr=track, tp=topic: self.open_track(tr, tp["id"]), width=9).pack(side="right")
        label(card, f'Разминка: {day["career_action"]["title"]}', size=9, color=MUTED,
              bg=card.cget("bg"), pack={"anchor": "w", "pady": (9, 0)})


class TrackWindow(tk.Toplevel):
    def __init__(self, master, track, store, on_change):
        super().__init__(master)
        self.track = track
        self.store = store
        self.on_change = on_change
        self.topics = [track["topics"][number - 1] for number in TRACK_PRIORITY[track["id"]]]
        self.topic_index = self.first_incomplete_topic()
        self.stage = self.first_stage(self.topics[self.topic_index])
        self.title(f'Job Search OS · {track["title"]}')
        self.geometry("1320x840")
        self.minsize(1080, 720)
        self.configure(bg=BG)
        self.build()

    def first_incomplete_topic(self):
        for index, topic in enumerate(self.topics):
            if not all(self.store.solved(task["id"]) for task in topic["tasks"]):
                return index
        return 0

    def first_stage(self, topic):
        if topic["id"] not in self.store.data["prompt_ready"]:
            return 0
        for index, task in enumerate(topic["tasks"], 1):
            if not self.store.solved(task["id"]):
                return index
        if topic.get("practice_links"):
            return len(topic["tasks"]) + 1
        return len(topic["tasks"])

    def build(self):
        for widget in self.winfo_children():
            widget.destroy()
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=28, pady=22)
        label(header, self.track["title"], size=24, bold=True, pack={"side": "left"})
        solved = sum(self.store.solved(task["id"]) for topic in self.track["topics"] for task in topic["tasks"])
        total = sum(len(topic["tasks"]) for topic in self.track["topics"])
        label(header, f"{solved}/{total} задач", size=11, color=self.track["color"], bold=True,
              pack={"side": "right"})
        shell = tk.Frame(self, bg=BG)
        shell.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        self.build_topics(shell)
        self.content = ScrollFrame(shell, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(16, 0))
        self.render_stage()

    def build_topics(self, parent):
        sidebar = tk.Frame(parent, bg=PANEL, width=320, highlightbackground=BORDER, highlightthickness=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        label(sidebar, "24 ТЕМЫ", size=9, color=MUTED, bold=True,
              pack={"anchor": "w", "padx": 16, "pady": (16, 8)})
        scroll = ScrollFrame(sidebar, bg=PANEL, width=300)
        scroll.pack(fill="both", expand=True)
        for index, topic in enumerate(self.topics):
            complete = all(self.store.solved(task["id"]) for task in topic["tasks"])
            active = index == self.topic_index
            unlocked = self.topic_unlocked(index)
            prefix = "✓" if complete else (f'{topic["number"]:02}' if unlocked else "🔒")
            tk.Button(scroll.inner, text=f'{prefix}  {topic["title"]}', command=lambda i=index: self.select_topic(i),
                      state="normal" if unlocked else "disabled",
                      disabledforeground="#56617A", bg=PANEL_2 if active else PANEL,
                      fg=SUCCESS if complete else TEXT,
                      activebackground=PANEL_2, activeforeground=TEXT, relief="flat", bd=0,
                      anchor="w", justify="left", wraplength=255, cursor="hand2",
                      font=(FONT, 10, "bold" if active else "normal"), padx=14, pady=10
                      ).pack(fill="x", padx=7, pady=2)

    def select_topic(self, index):
        if not self.topic_unlocked(index):
            previous = self.topics[index - 1]
            messagebox.showinfo(
                "Тема закрыта",
                f"Сначала закончи предыдущую тему: в ней {len(previous['tasks'])} заданий.",
                parent=self,
            )
            return
        self.topic_index = index
        self.stage = self.first_stage(self.topics[index])
        self.build()

    def open_topic_id(self, topic_id):
        for index, topic in enumerate(self.topics):
            if topic["id"] == topic_id:
                self.select_topic(index)
                return

    def topic_unlocked(self, index):
        return all(
            all(self.store.solved(task["id"]) for task in topic["tasks"])
            for topic in self.topics[:index]
        )

    @property
    def topic(self):
        return self.topics[self.topic_index]

    def render_stage(self):
        parent = self.content.inner
        label(parent, f'{self.track["number"]}.{self.topic["number"]:02}  {self.topic["title"]}',
              size=22, bold=True, pack={"anchor": "w", "pady": (4, 4)})
        label(parent, "Урок → практика → тема завершена.",
              color=MUTED, pack={"anchor": "w", "pady": (0, 14)})
        self.render_completion_status(parent)
        self.render_steps(parent)
        if self.stage == 0:
            self.render_prompt(parent)
        elif self.stage <= len(self.topic["tasks"]):
            self.render_task(parent, self.stage - 1)
        else:
            self.render_practice(parent)
        self.content.top()

    def render_completion_status(self, parent):
        studied = topic_studied(self.store, self.topic)
        box = tk.Frame(parent, bg="#11253A", padx=14, pady=11,
                       highlightbackground=SUCCESS if studied else BORDER, highlightthickness=1)
        box.pack(fill="x", pady=(0, 12))
        if studied:
            text_value = "ТЕМА ЗАВЕРШЕНА"
            color = SUCCESS
        else:
            text_value = "ТЕМА В РАБОТЕ"
            color = MUTED
        label(box, text_value, size=9, color=color, bold=True, bg="#11253A", pack={"side": "left"})

    def render_steps(self, parent):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 18))
        tasks = self.topic["tasks"]
        titles = ["Урок"] + [task.get("tab_label", str(index + 1)) for index, task in enumerate(tasks)]
        if self.topic.get("practice_links"):
            titles.append("Экзамен +" if self.topic.get("exam") else "Практика")
        prompt_done = self.topic["id"] in self.store.data["prompt_ready"]
        for index, title in enumerate(titles):
            if index == 0:
                done = prompt_done
                locked = False
            elif index <= len(tasks):
                done = self.store.solved(tasks[index - 1]["id"])
                locked = not prompt_done or not all(self.store.solved(task["id"]) for task in tasks[:index - 1])
            else:
                done = all(self.store.solved(task["id"]) for task in tasks)
                locked = not done
            bg = self.track["color"] if index == self.stage else ("#17392F" if done else PANEL)
            fg = "#07131A" if index == self.stage else (SUCCESS if done else MUTED)
            control = tk.Label(row, text=("🔒 " if locked else "") + title, bg=bg, fg=fg,
                               font=(FONT, 9, "bold"), padx=12, pady=9, width=12)
            columns = min(4, len(titles))
            control.grid(row=index // columns, column=index % columns, sticky="ew", padx=(0, 7), pady=(0, 7))
            row.grid_columnconfigure(index % columns, weight=1)
            if not locked:
                control.configure(cursor="hand2")
                control.bind("<Button-1>", lambda _e, s=index: self.go_stage(s))

    def go_stage(self, stage):
        if stage > 0 and self.topic["id"] not in self.store.data["prompt_ready"]:
            return
        tasks = self.topic["tasks"]
        if 1 < stage <= len(tasks) and not all(self.store.solved(task["id"]) for task in tasks[:stage - 1]):
            return
        if stage > len(tasks) and not all(self.store.solved(task["id"]) for task in tasks):
            return
        self.stage = stage
        self.build()

    def section(self, parent, title, body=None, color=TEXT):
        box = tk.Frame(parent, bg=PANEL, padx=20, pady=16, highlightbackground=BORDER, highlightthickness=1)
        box.pack(fill="x", pady=(0, 12))
        label(box, title, size=9, color=color, bold=True, pack={"anchor": "w", "pady": (0, 8)})
        if body:
            label(box, body, size=11, color=TEXT, wrap=850, pack={"anchor": "w", "fill": "x"})
        return box

    def render_prompt(self, parent):
        label(parent, "Сначала пройди полный урок", size=16, bold=True,
              pack={"anchor": "w", "pady": (0, 10)})
        label(parent, "Сначала преподаватель даст подробную теорию для конспекта. Проверка начнётся только после твоего согласия.",
              color=MUTED, wrap=850, pack={"anchor": "w", "pady": (0, 12)})
        actions = tk.Frame(parent, bg=BG)
        actions.pack(fill="x", pady=(0, 12))
        button(actions, "Скопировать промпт", self.copy_prompt, primary=True).pack(side="left")
        button(actions, "Я закончил разбор →", self.finish_prompt).pack(side="right")
        box = self.section(parent, "ГОТОВЫЙ ПРОМПТ", color=self.track["color"])
        text_shell = tk.Frame(box, bg="#0D1425")
        text_shell.pack(fill="both", expand=True)
        text = tk.Text(text_shell, height=19, bg="#0D1425", fg=TEXT, insertbackground=TEXT,
                       relief="flat", wrap="word", font=("Consolas", 10), padx=14, pady=12)
        text.insert("1.0", self.topic["mentor_prompt"])
        text.configure(state="disabled")
        prompt_bar = ttk.Scrollbar(text_shell, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=prompt_bar.set)
        prompt_bar.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        text.bind("<MouseWheel>", lambda event: self.scroll_prompt(text, event))

    @staticmethod
    def scroll_prompt(text, event):
        if not event.delta:
            return None
        units = max(1, abs(event.delta) // 120)
        text.yview_scroll(-units if event.delta > 0 else units, "units")
        return "break"

    def copy_prompt(self):
        self.clipboard_clear()
        self.clipboard_append(self.topic["mentor_prompt"])
        self.update()
        messagebox.showinfo("Готово", "Промпт скопирован. Вернись после занятия и продолжи с первой задачи.", parent=self)

    def finish_prompt(self):
        self.store.mark_prompt(self.topic["id"])
        self.stage = 1
        self.build()
        self.on_change()

    def render_task(self, parent, task_index):
        task = self.topic["tasks"][task_index]
        record = self.store.data["task_records"].get(task["id"], {})
        label(parent, task["label"], size=9, color=self.track["color"], bold=True,
              pack={"anchor": "w", "pady": (0, 5)})
        label(parent, task["title"], size=17, bold=True, pack={"anchor": "w", "pady": (0, 14)})
        self.section(parent, "УСЛОВИЕ", task["statement"], self.track["color"])
        self.section(parent, "РЕЗУЛЬТАТ", task["deliverable"])
        if task.get("exam_prompt"):
            exam_actions = tk.Frame(parent, bg=BG)
            exam_actions.pack(fill="x", pady=(0, 12))
            button(exam_actions, "Скопировать экзаменационный промпт", lambda: self.copy_exam_prompt(task),
                   primary=True).pack(side="left")
        if task.get("external_url"):
            links = tk.Frame(parent, bg=BG)
            links.pack(fill="x", pady=(0, 12))
            button(links, task["external_label"] + " ↗",
                   lambda: webbrowser.open(task["external_url"]), primary=True).pack(side="left")
        self.render_solution(parent, task, record)

    def copy_exam_prompt(self, task):
        self.clipboard_clear()
        self.clipboard_append(task["exam_prompt"])
        self.update()
        messagebox.showinfo("Готово", "Экзаменационный промпт скопирован. Проходи его в новом чате.", parent=self)

    def render_practice(self, parent):
        exam = self.topic.get("exam")
        if exam:
            label(parent, "Итоговый экзамен направления", size=17, bold=True,
                  pack={"anchor": "w", "pady": (0, 7)})
            label(parent, "Экзамен проверит весь раздел и выдаст балл, пробелы и честный вердикт готовности.",
                  color=MUTED, wrap=850, pack={"anchor": "w", "pady": (0, 12)})
            exam_card = tk.Frame(parent, bg="#18233D", padx=18, pady=16,
                                 highlightbackground=self.track["color"], highlightthickness=1)
            exam_card.pack(fill="x", pady=(0, 18))
            label(exam_card, exam["title"], size=12, bold=True, bg="#18233D", pack={"anchor": "w"})
            label(exam_card, exam["statement"], color=MUTED, bg="#18233D", wrap=820,
                  pack={"anchor": "w", "fill": "x", "pady": (5, 12)})
            button(exam_card, "Скопировать экзамен", lambda: self.copy_exam_prompt(exam),
                   primary=True).pack(anchor="w")

        label(parent, "Дополнительная практика", size=17, bold=True,
              pack={"anchor": "w", "pady": (0, 7)})
        label(parent, "Эти задачи закрепляют навык и не влияют на прогресс темы.", color=MUTED,
              pack={"anchor": "w", "pady": (0, 14)})
        for item in self.topic.get("practice_links", []):
            card = tk.Frame(parent, bg=PANEL, padx=18, pady=15,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", pady=(0, 9))
            info = tk.Frame(card, bg=PANEL)
            info.pack(side="left", fill="x", expand=True)
            label(info, item["title"], size=11, bold=True, pack={"anchor": "w"})
            label(info, f'{item["difficulty"]} · Цель: {item["target"]}', color=MUTED, wrap=650,
                  pack={"anchor": "w", "pady": (4, 0)})
            button(card, "Открыть LeetCode ↗", lambda url=item["url"]: webbrowser.open(url)).pack(side="right")
        actions = tk.Frame(parent, bg=BG)
        actions.pack(fill="x", pady=(10, 0))
        if self.topic_index < len(self.topics) - 1:
            button(actions, "Следующая тема →", self.advance_topic, primary=True).pack(side="right")
        else:
            label(actions, "Направление завершено", color=SUCCESS, bold=True, pack={"side": "right"})

    def advance_topic(self):
        if self.topic_index < len(self.topics) - 1:
            self.topic_index += 1
            self.stage = self.first_stage(self.topics[self.topic_index])
            self.build()
            self.on_change()

    def list_section(self, parent, title, items, color=TEXT):
        box = self.section(parent, title, color=color)
        for item in items:
            label(box, f"• {item}", size=10, wrap=840,
                  pack={"anchor": "w", "fill": "x", "pady": 3})

    def task_path(self, task):
        return WORKSPACE / self.track["id"] / self.topic["id"] / task["id"]

    def render_solution(self, parent, task, record):
        box = self.section(parent, "МОЙ ОТВЕТ", color=WARNING)
        path = self.task_path(task)
        if record:
            color = SUCCESS if record.get("status") == "solved" else DANGER
            result = "Решено" if record.get("status") == "solved" else "Нужно повторить"
            label(box, f'{result} · {record.get("updated_at", "")}', color=color, bold=True,
                  pack={"anchor": "w", "pady": (7, 0)})
        if task.get("kind") == "code" and not task.get("external_url"):
            actions = tk.Frame(box, bg=PANEL)
            actions.pack(fill="x", pady=(8, 10))
            button(actions, "Открыть файл для кода", lambda: self.open_solution(task), primary=True).pack(side="left")
            label(actions, "необязательно", color=MUTED, pack={"side": "left", "padx": 10})
        answer_label = "Объяснение своими словами" if task.get("kind") == "theory" else "Ответ или заметка о решении"
        label(box, answer_label, color=MUTED, pack={"anchor": "w", "pady": (4, 5)})
        notes = tk.Text(box, height=7 if task.get("kind") == "theory" else 5, bg="#0D1425", fg=TEXT, insertbackground=TEXT,
                        relief="flat", wrap="word", font=(FONT, 10), padx=10, pady=8)
        notes.insert("1.0", record.get("note", ""))
        notes.pack(fill="x")
        submit = tk.Frame(box, bg=PANEL)
        submit.pack(fill="x", pady=(10, 0))
        button(submit, "Повторить позже", lambda: self.submit_task(task, notes, "retry")).pack(side="left")
        button(submit, "Готово →", lambda: self.submit_task(task, notes, "solved"), primary=True).pack(side="right")
        attempts = record.get("attempts", [])
        if attempts:
            label(box, f"Попыток: {len(attempts)}", color=MUTED, pack={"anchor": "w", "pady": (10, 0)})

    def starter_files(self, task):
        if task.get("kind") == "exam":
            return {"exam-report.md": "# Итоговый экзамен\n\n## Балл\n\n## Вердикт\n\n## Пробелы\n"}
        if task.get("kind") == "theory":
            return {}
        if self.track["id"] in {"python", "async", "algorithms"}:
            return {"solution.py": "\"\"\"Напиши запускаемое решение конкретной задачи здесь.\"\"\"\n\n",
                    "input.jsonl": "", "result.txt": "Ожидаемый и фактический результат:\n"}
        if self.track["id"] == "sql":
            return {"schema.sql": "-- Схема и тестовые данные\n", "solution.sql": "-- Решение\n",
                    "result.txt": "Ожидаемый и фактический результат:\n"}
        if self.track["id"] in {"linux", "git"}:
            return {"solution.sh": "#!/usr/bin/env bash\nset -Eeuo pipefail\n",
                    "transcript.txt": "Команды и фактический вывод:\n"}
        if self.track["id"] == "docker":
            return {"Dockerfile": "# Решение\n", "compose.yaml": "services:\n",
                    "verify.txt": "Команды проверки и вывод:\n"}
        if self.track["id"] == "http":
            return {"requests.http": "# Запросы для воспроизведения\n", "answer.md": "# Решение\n"}
        if self.track["id"] == "testing":
            return {"implementation.py": "\"\"\"Минимальный компонент для проверки.\"\"\"\n",
                    "test_solution.py": "\"\"\"Отдельный pytest-модуль.\"\"\"\n"}
        return {"models.py": "# Модели или запросы ORM по условию\n",
                "serializers.py": "# Схема входа и выхода при необходимости\n",
                "views.py": "# Сценарий запроса при необходимости\n",
                "result.txt": "Команда запуска и фактический результат:\n"}

    def open_solution(self, task):
        path = self.task_path(task)
        path.mkdir(parents=True, exist_ok=True)
        readme = path / "README.md"
        if not readme.exists():
            readme.write_text(
                f"# {task['title']}\n\n## Условие\n{task['statement']}\n\n"
                f"## Что сохранить\n{task['deliverable']}\n\n"
                "## Результат\n- Команда запуска:\n- Фактический результат:\n- Что понял или исправил:\n",
                encoding="utf-8",
            )
        for name, content in self.starter_files(task).items():
            file = path / name
            if not file.exists():
                file.write_text(content, encoding="utf-8")
        candidates = [name for name in self.starter_files(task) if name.endswith((".py", ".sql", ".http", ".sh"))]
        os.startfile(path / candidates[0] if candidates else path)

    def submit_task(self, task, notes, status):
        note = notes.get("1.0", "end").strip()
        path = self.task_path(task) if self.task_path(task).exists() else None
        self.store.record(task["id"], status, path, note)
        if status == "solved":
            if self.stage < len(self.topic["tasks"]):
                self.stage += 1
            elif self.topic.get("practice_links"):
                self.stage = len(self.topic["tasks"]) + 1
            elif self.topic_index < len(self.topics) - 1:
                self.topic_index += 1
                self.stage = self.first_stage(self.topics[self.topic_index])
        self.build()
        self.on_change()


if __name__ == "__main__":
    enable_dpi_awareness()
    LearningApp().mainloop()
