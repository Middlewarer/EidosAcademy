"""Hard-mode dates, discipline and reversible state migration; no network."""
from datetime import date
from urllib.parse import urlparse

START = date(2026, 10, 2)
TARGET = date(2026, 12, 15)
CHECKPOINTS = (
    ("2026-10-19", "Python Core: коротко применить изученную тему без подсказок и объяснить результат."),
    ("2026-11-11", "SQL / HTTP: защитить схему данных, запрос и путь HTTP-запроса."),
    ("2026-11-24", "API: контракт, права доступа, обработка ошибок и интеграционный тест."),
    ("2026-12-04", "Проект: воспроизводимый запуск и защита самостоятельно выполненного изменения."),
    ("2026-12-12", "Три независимых пробных интервью ≥85/100 без подсказок и критических ошибок."),
    ("2026-12-15", "Цель выхода на работу. Оффер зависит от работодателя, дата не гарантирована."),
)
DISCIPLINE = (
    "До подсказки — собственная попытка. После подсказки — новое решение с нуля.",
    "Завершение задачи: результат, проверка, объяснение. Прочитанный ответ не считается.",
    "Ошибка получает причину, исправление и дату повторной проверки.",
    "Пропущенный день не списывает долг и не требует бессонной компенсации.",
    "Не можешь объяснить строку кода — не заявляй её как самостоятельную работу.",
    "Один рабочий блок — одна задача. Телефон и посторонние вкладки закрыты.",
    "Оценивай воспроизводимый результат, а не количество открытых уроков.",
)


def discipline(today=None):
    return DISCIPLINE[((today or date.today()) - START).days % len(DISCIPLINE)]


def migrate(payload):
    if payload.get("preparation_mode") == "hard-2026-10-02-v1":
        return False
    archive = payload.setdefault("integration_archive", {})
    imported, manual = [], []
    for item in payload.get("applications", []):
        host = urlparse(str(item.get("url", ""))).hostname or ""
        is_remote = (item.get("source") in {"browser", "hh", "hh-planned", "hh-pending-sync"}
                     or host == "hh.ru" or host.endswith(".hh.ru"))
        (imported if is_remote else manual).append(item)
    archive.setdefault("applications", []).extend(imported)
    payload["applications"] = manual
    for key in ("hh_sync", "job_search", "letter_ai"):
        if key in payload:
            archive[key] = payload.pop(key)
    archive.setdefault("previous_start_date", payload.get("start_date"))
    archive.setdefault("previous_daily_target_hours", payload.get("daily_target_hours"))
    payload["start_date"] = START.isoformat()
    payload["target_date"] = TARGET.isoformat()
    payload["daily_target_hours"] = 9
    payload["preparation_mode"] = "hard-2026-10-02-v1"
    return True
