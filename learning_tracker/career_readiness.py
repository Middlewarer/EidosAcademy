"""Измеримая готовность к найму: знания, доказательства, интервью и рынок."""

from __future__ import annotations

from datetime import date

from daily_plan import ROADMAP_PHASES, TRACK_PRIORITY
from mastery_curriculum import CURRICULUM
from manual_applications import is_submitted
from preparation import TARGET


DEADLINE = TARGET
VERIFICATION_SCORE = 80

PROJECTS = [
    {
        "id": "eidos-proof",
        "title": "EidosAcademy: доказательство production-навыков",
        "description": "Не считать весь проект доказательством автоматически, а отдельно защитить ключевые инженерные решения.",
        "milestones": [
            ("architecture", "Архитектура", "Схема запроса от браузера до PostgreSQL и объяснение границ React, Nginx, Django, Redis и Caddy."),
            ("api", "API-контракт", "Один критический endpoint: контракт, валидация, права, ошибки и интеграционный тест."),
            ("database", "Данные и производительность", "ER-схема, инварианты БД, демонстрация запроса и разбор его плана."),
            ("security", "Безопасность", "Threat model для auth/upload/API и доказательство минимум трёх защитных мер."),
            ("operations", "Эксплуатация", "Runbook деплоя, healthcheck, backup/restore и диагностика одного искусственного сбоя."),
        ],
    },
    {
        "id": "order-service",
        "title": "Order Service: транзакционный backend",
        "description": "Небольшой сервис, который доказывает SQL, API, транзакции, идемпотентность и тестирование независимо от EidosAcademy.",
        "milestones": [
            ("contract", "Контракт и модель", "OpenAPI, схема данных, ограничения и явные бизнес-инварианты заказа."),
            ("transaction", "Конкурентный сценарий", "Резервирование товара без oversell, повтор запроса без дубля и объяснение блокировок."),
            ("tests", "Набор проверок", "Unit и integration-тесты, включая конфликт, повтор, rollback и чужой ресурс."),
            ("delivery", "Запуск", "Docker Compose, миграции, healthcheck, README и одна воспроизводимая команда проверки."),
        ],
    },
    {
        "id": "async-integration",
        "title": "Async Integration Service",
        "description": "Финальный проект для Asyncio/FastAPI после подтверждения основного Django-backend стека.",
        "milestones": [
            ("concurrency", "Управление конкурентностью", "Timeout, cancellation, semaphore/backpressure и отсутствие потерянных задач."),
            ("reliability", "Надёжная интеграция", "Ограниченные retries, backoff, идемпотентность и обработка частичного отказа."),
            ("observability", "Наблюдаемость", "Request ID, структурированные логи, метрики и сценарий диагностики."),
            ("tests", "Async-тесты", "Проверки timeout, cancellation, ошибки внешнего API и корректного завершения."),
        ],
    },
]


RESUME_CHECKLIST = [
    ("one_page", "Резюме укладывается в одну страницу и начинается с целевой роли."),
    ("facts", "Каждый сильный тезис подтверждён ссылкой, цифрой, тестом или конкретным решением."),
    ("project_case", "EidosAcademy описан как задача → решение → результат, а не перечень технологий."),
    ("links", "GitHub, рабочий сайт и контакты открываются без запроса доступа."),
    ("pitch", "Подготовлен рассказ о себе на 60–90 секунд без общих фраз."),
    ("variants", "Есть отдельные варианты под backend, automation/support и AQA при необходимости."),
]


def _phase_topic_ids(phase_ids):
    tracks = {track["id"]: track for track in CURRICULUM}
    result = []
    for phase in ROADMAP_PHASES:
        if phase["id"] not in phase_ids:
            continue
        for track_id, first, last in phase["segments"]:
            topic_numbers = TRACK_PRIORITY[track_id][first - 1:last]
            result.extend(tracks[track_id]["topics"][number - 1]["id"] for number in topic_numbers)
    return result


CORE_TOPIC_IDS = set(_phase_topic_ids({
    "foundation", "backend-start", "working-backend",
}))


def topic_studied(store, topic):
    return (
        topic["id"] in store.data.get("prompt_ready", [])
        and all(store.solved(task["id"]) for task in topic["tasks"])
    )


def verification_record(store, topic_id):
    return store.data.get("verification_records", {}).get(topic_id, {})


def topic_verified(store, topic_id):
    record = verification_record(store, topic_id)
    return record.get("status") == "verified" and int(record.get("score", 0)) >= VERIFICATION_SCORE


def verification_prompt(track, topic):
    tasks = "\n".join(f'- {task["title"]}: {task["statement"]}' for task in topic["tasks"])
    return f"""Ты — независимый технический интервьюер. Проверь навык по теме «{topic['title']}» направления «{track['title']}» на уровне уверенного junior Python backend developer.

Это проверка, а не урок. Не пересказывай теорию и не подсказывай до завершения моей попытки.

Обязательное ядро: {topic['theory']}
Критическая типичная ошибка: {topic['pitfall']}
Практика, которую я должен уметь объяснить или выполнить:
{tasks}

До начала молча составь матрицу из шести разных целей и исключи смысловые повторы:
1) объяснение механизма;
2) прогноз поведения небольшого примера;
3) поиск причины ошибки;
4) исправление решения;
5) выбор подхода с компромиссами;
6) новый backend-сценарий на перенос знания.

Задавай пункты по одному. Не повторяй и не перефразируй уже проверенную мысль. Разрешено только одно уточнение к неполному ответу. Для практического пункта требуй ход рассуждений, проверку результата и граничный случай.

После шести пунктов выдай строгий отчёт:
- балл 0–100;
- результат по каждой цели;
- критические ошибки;
- что доказано ответами, а что пока только заявлено;
- один повторный шаг для каждого пробела;
- вердикт VERIFIED только при балле не ниже {VERIFICATION_SCORE}, отсутствии критической ошибки и самостоятельном решении практического пункта; иначе RETRY.

Начни сразу с пункта №1."""


def project_progress(store):
    records = store.data.get("project_records", {})
    total = sum(len(project["milestones"]) for project in PROJECTS)
    done = 0
    for project in PROJECTS:
        completed = records.get(project["id"], {})
        done += sum(bool(completed.get(item_id, {}).get("evidence")) for item_id, _title, _description in project["milestones"])
    return done, total


def readiness_summary(store):
    topics = [topic for track in CURRICULUM for topic in track["topics"]]
    studied = [topic for topic in topics if topic_studied(store, topic)]
    verified = [topic for topic in topics if topic_verified(store, topic["id"])]
    core = [topic for topic in topics if topic["id"] in CORE_TOPIC_IDS]
    core_studied = [topic for topic in core if topic_studied(store, topic)]
    project_done, project_total = project_progress(store)

    interviews = [s for s in store.data.get("interview_sessions", [])
                  if s.get("mode", "technical") != "diagnostic" and not s.get("assisted")][-5:]
    interview_score = round(sum(item.get("score", 0) for item in interviews) / len(interviews)) if interviews else 0
    resume_done = sum(bool(store.data.get("resume_checklist", {}).get(key)) for key, _label in RESUME_CHECKLIST)
    applications = [
        item for item in store.data.get("applications", [])
        if is_submitted(item)
    ]
    active_applications = sum(item.get("status") not in {"rejected", "offer"} for item in applications)

    # A completed topic is final for learning progress. Verification records are
    # kept as a separate skill-matrix aid and do not gate readiness.
    knowledge = round(len(core_studied) / len(core) * 100) if core else 0
    proof = round(project_done / project_total * 100) if project_total else 0
    resume = round(resume_done / len(RESUME_CHECKLIST) * 100)
    market = min(100, len(applications) * 2 + active_applications * 3)
    interview = interview_score
    # Отклики остаются наблюдаемой метрикой, но не повышают техническую
    # готовность. Иначе трекер начинает оптимизировать число заявок вместо навыка.
    overall = round(knowledge * 0.45 + proof * 0.25 + interview * 0.2 + resume * 0.1)
    return {
        "studied": len(studied),
        "verified": len(verified),
        "total_topics": len(topics),
        "core_verified": len(core_studied),
        "core_total": len(core),
        "knowledge": knowledge,
        "proof": proof,
        "interview": interview,
        "resume": resume,
        "market": market,
        "overall": overall,
        "project_done": project_done,
        "project_total": project_total,
        "applications": len(applications),
        "active_applications": active_applications,
        "days_left": max(0, (DEADLINE - date.today()).days),
    }
