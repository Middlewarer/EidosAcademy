"""Расчёты для экранов «Сегодня», недельного отчёта и собеседования."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from daily_plan import build_daily_plan
from career_readiness import topic_studied
from mastery_curriculum import CURRICULUM
from manual_applications import is_submitted


def week_bounds(value=None):
    current = value or date.today()
    if isinstance(current, str):
        current = datetime.strptime(current, "%Y-%m-%d").date()
    start = current - timedelta(days=current.weekday())
    return start, start + timedelta(days=6)


def calendar_day(value=None):
    """Возвращает план именно календарного дня, не подменяя его долгами."""
    current = value or date.today()
    if isinstance(current, str):
        current = datetime.strptime(current, "%Y-%m-%d").date()
    plan = build_daily_plan()
    exact = next((item for item in plan if item["date"] == current), None)
    upcoming = next((item for item in plan if item["date"] > current), None)
    return exact, upcoming


def overdue_tasks(store, value=None):
    current = value or date.today()
    if isinstance(current, str):
        current = datetime.strptime(current, "%Y-%m-%d").date()
    result = []
    for day in build_daily_plan():
        if day["date"] >= current:
            break
        for track, topic in day["topics"]:
            pending = [task for task in topic["tasks"] if not store.solved(task["id"])]
            if pending:
                result.append({"day": day, "track": track, "topic": topic, "tasks": pending})
    return result


def _attempt_date(attempt):
    try:
        return datetime.fromisoformat(attempt.get("at", "")).date()
    except (TypeError, ValueError):
        return None


def weekly_summary(store, anchor=None):
    start, end = week_bounds(anchor)
    plan_days = [day for day in build_daily_plan() if start <= day["date"] <= end]
    today = date.today()
    due_days = [day for day in plan_days if day["date"] <= today] if start <= today else []
    week_ids = {task_id for day in plan_days for task_id in day["task_ids"]}
    planned_ids = {task_id for day in due_days for task_id in day["task_ids"]}
    solved_planned = planned_ids & set(store.data["completed"])

    solved_this_week = set()
    attempts_this_week = 0
    for task_id, record in store.data.get("task_records", {}).items():
        for attempt in record.get("attempts", []):
            attempt_day = _attempt_date(attempt)
            if attempt_day and start <= attempt_day <= end:
                attempts_this_week += 1
                if attempt.get("status") == "solved":
                    solved_this_week.add(task_id)

    focus_seconds = 0
    sessions = 0
    active_days = 0
    for offset in range(7):
        key = (start + timedelta(days=offset)).isoformat()
        seconds = int(store.data.get("work_seconds", {}).get(key, 0))
        day_sessions = int(store.data.get("pomodoro_sessions", {}).get(key, 0))
        focus_seconds += seconds
        sessions += day_sessions
        if seconds or day_sessions:
            active_days += 1

    verified_this_week = 0
    for record in store.data.get("verification_records", {}).values():
        verified_day = _attempt_date({"at": record.get("at", "")})
        if record.get("status") == "verified" and verified_day and start <= verified_day <= end:
            verified_this_week += 1

    applications_this_week = 0
    for application in store.data.get("applications", []):
        if not is_submitted(application):
            continue
        application_day = _attempt_date({"at": application.get("submitted_at") or (
            application.get("created_at", "") if application.get("source") != "browser" else "")})
        if application_day and start <= application_day <= end:
            applications_this_week += 1

    career_actions = sum(
        start.isoformat() <= key[:10] <= end.isoformat()
        for key in store.data.get("career_actions", {})
        if len(key) >= 10
    )

    by_track = []
    for track in CURRICULUM:
        ids = {task["id"] for topic in track["topics"] for task in topic["tasks"]}
        planned = len(planned_ids & ids)
        completed = len(solved_planned & ids)
        if planned or completed:
            by_track.append({"track": track, "planned": planned, "completed": completed})

    percent = round(len(solved_planned) / len(planned_ids) * 100) if planned_ids else 0
    return {
        "start": start,
        "end": end,
        "plan_days": plan_days,
        "week_planned": len(week_ids),
        "planned": len(planned_ids),
        "completed_planned": len(solved_planned),
        "completed_this_week": len(solved_this_week),
        "attempts": attempts_this_week,
        "focus_seconds": focus_seconds,
        "sessions": sessions,
        "active_days": active_days,
        "verified_this_week": verified_this_week,
        "applications_this_week": applications_this_week,
        "career_actions": career_actions,
        "percent": percent,
        "by_track": by_track,
    }


def completed_topics(store, track):
    return [
        topic for topic in track["topics"]
        if topic_studied(store, topic)
    ]


def interview_prompt(track, topics, focus=""):
    names = ", ".join(topic["title"] for topic in topics)
    focus_text = focus.strip() or "без дополнительного акцента"
    return f"""Проведи со мной пробное техническое собеседование на позицию Junior Python Backend Developer.

Направление: {track['title']}.
Темы, которые я уже прошёл и по которым меня можно проверять: {names}.
Дополнительный акцент: {focus_text}.

Проведи собеседование как живой интервьюер:
— задай 8 вопросов по одному и жди моего ответа после каждого;
— до начала молча составь матрицу из 8 разных навыков; каждый вопрос должен проверять отдельный навык или механизм;
— используй ровно один вопрос каждого типа: объяснение механизма, прогноз результата, чтение кода, поиск ошибки, исправление решения, выбор с компромиссами, граничный случай и backend-сценарий;
— не повторяй вопрос и не перефразируй уже проверенную мысль; одно уточнение допустимо только к неполному ответу и не считается новым вопросом;
— не спрашивай темы вне указанного списка;
— не подсказывай правильный ответ до моей попытки;
— после каждого ответа дай одну короткую реплику, а подробный разбор сохрани до конца;
— один из вопросов сделай практическим: небольшой фрагмент кода, SQL, конфигурации или алгоритмическая задача в зависимости от направления;
— уточняй ответ, если он поверхностный, как это сделал бы технический интервьюер.

В конце оцени отдельно: точность знаний, ход рассуждений, качество кода и ясность речи. Дай общий балл от 0 до 100, перечисли сильные стороны, конкретные ошибки и максимум три темы для повторения. Вердикт: «готов к junior-собеседованию», «нужна небольшая доработка» или «нужно повторить базу».

Начни с приветствия и вопроса №1."""

