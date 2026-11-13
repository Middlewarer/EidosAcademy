"""Persistent spaced-retrieval ledger, separate from legacy completion data."""
import json
import os
import tempfile
import threading
from datetime import date, timedelta
from pathlib import Path

LOCK = threading.RLock()
GAPS = [0, 1, 2, 4, 7]
START = "2026-10-27"
TARGET = "2026-11-30"


def read_state(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"version": 1, "records": {}}


def due_date(topic, record):
    stage = record.get("stage", 0)
    if stage >= 5:
        return None
    if record.get("retry_on"):
        return record["retry_on"]
    if not stage:
        return topic["scheduled"]
    return (date.fromisoformat(record["passed_on"]) + timedelta(days=GAPS[stage])).isoformat()


def snapshot(path, course, today=None):
    today = today or date.today().isoformat()
    with LOCK:
        state = read_state(path)
        return {"today": today, "start": START, "target": TARGET, "records": state["records"],
                "due": {topic["id"]: due_date(topic, state["records"].get(topic["id"], {})) for topic in course}}


def record_attempt(path, progress_path, course, body, today=None):
    today = today or date.today().isoformat()
    topic = next((item for item in course if item["id"] == body.get("topic_id")), None)
    if not topic or body.get("rating") not in ("pass", "retry"):
        raise ValueError("Неизвестная тема или результат")
    answer = str(body.get("answer", "")).strip()
    if not 20 <= len(answer) <= 12000:
        raise ValueError("Запишите ответ по памяти: от 20 до 12000 символов")
    with LOCK:
        state = read_state(path)
        record = state["records"].get(topic["id"], {"stage": 0, "attempts": []})
        if body.get("stage") != record["stage"]:
            raise ValueError("Этап уже изменился. Обновите план")
        due = due_date(topic, record)
        if due is None or today < due:
            raise ValueError("Повтор ещё не наступил: интервалы нельзя закрыть заранее")
        if body["rating"] == "pass":
            progress = json.loads(progress_path.read_text(encoding="utf-8-sig"))
            if not set(topic["task_ids"]).issubset(set(progress.get("completed", []))):
                raise ValueError("Сначала выполните все задания темы")
            if len(str(body.get("evidence", "")).strip()) < 8:
                raise ValueError("Укажите файл решения или конкретный проверенный пример")
            record["stage"] += 1
            record["passed_on"] = today
            record.pop("retry_on", None)
        else:
            record["retry_on"] = (date.fromisoformat(today) + timedelta(days=1)).isoformat()
        record["attempts"].append({"at": today, "stage": body["stage"], "rating": body["rating"],
                                   "answer": answer, "evidence": str(body.get("evidence", ""))[:2000]})
        state["records"][topic["id"]] = record
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.with_suffix(".last-good.json").write_bytes(path.read_bytes())
        fd, name = tempfile.mkstemp(prefix=".hard-mode-", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(state, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, path)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    return snapshot(path, course, today)
