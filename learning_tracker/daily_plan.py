"""Карьерный план: сначала частые junior-темы, затем production и специализация."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from mastery_curriculum import CURRICULUM


START_DATE = date(2026, 10, 2)

# Девятичасовой план отдаёт почти всё время обучению, практике и независимой
# проверке навыка. Рынок остаётся короткой разминкой, а не отдельной сменой.
TARGET_MINUTES = 9 * 60
SOFT_MINUTES = 8 * 60
MAX_MINUTES = 9 * 60
LEARNING_TARGET_MINUTES = 7 * 60 + 10
LEARNING_MAX_MINUTES = 7 * 60 + 25
VERIFICATION_MINUTES = 75
CAREER_MINUTES = 20
REVIEW_MINUTES = 45
THEORY_MINUTES_PER_TOPIC = 35


# Приоритет внутри каждого направления. Значения — стабильные номера тем в
# CURRICULUM: прогресс пользователя не мигрирует и не теряется. Порядок выбран
# по зависимостям и частоте применения в работе junior Python backend, а не по
# историческому расположению темы в исходном списке.
TRACK_PRIORITY = {
    "python": [1, 2, 3, 4, 5, 6, 7, 10, 12, 19, 20, 21, 11, 8, 9, 13, 14, 16, 15, 24, 17, 18, 22, 23],
    "algorithms": [1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 9, 10, 17, 11, 12, 16, 20, 19, 21, 22, 18, 23, 24],
    "git": [1, 2, 19, 3, 4, 9, 5, 7, 10, 13, 8, 6, 23, 11, 12, 15, 14, 16, 21, 22, 24, 17, 18, 20],
    "linux": [1, 2, 3, 4, 6, 13, 5, 7, 8, 9, 10, 11, 21, 24, 12, 14, 15, 16, 19, 20, 18, 22, 23, 17],
    "sql": [1, 2, 3, 4, 15, 8, 13, 5, 6, 9, 10, 11, 12, 16, 20, 14, 17, 7, 18, 19, 21, 22, 24, 23],
    "http": [1, 2, 3, 4, 6, 7, 5, 10, 11, 8, 9, 12, 13, 19, 17, 20, 21, 22, 23, 24, 14, 15, 16, 18],
    "testing": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 12, 23, 24, 14, 16, 13, 15, 17, 18, 11, 21, 22],
    "django": [1, 2, 3, 4, 6, 7, 8, 15, 5, 9, 10, 11, 12, 13, 19, 16, 21, 22, 17, 18, 20, 23, 14, 24],
    "docker": [1, 2, 15, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 16, 18, 20, 21, 23, 24, 19, 22],
    "async": [1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 7, 8, 9, 17, 18, 10, 11, 19, 20, 21, 22, 12, 23, 24],
}


DAILY_QUESTS = [
    {
        "id": "interview-sprint",
        "title": "Спринт собеседования",
        "description": "Ответь без конспекта на пять коротких вопросов и сохрани два места, где ответ был неточным.",
        "instruction": "Проведи мини-собеседование из 5 вопросов по темам {topics}. До начала молча выбери 5 разных целей: механизм, чтение примера, ошибка, выбор подхода и перенос в новую ситуацию. Задавай по одному, не подсказывай до ответа. Не повторяй один факт и не перефразируй предыдущий вопрос. В конце назови две слабые точки и один сильный ответ.",
    },
    {
        "id": "bug-hunt",
        "title": "Охота на баги",
        "description": "Найди ошибки в небольшом примере раньше, чем AI покажет разбор.",
        "instruction": "Создай короткий внутренне согласованный пример с тремя принципиально разными реалистичными ошибками по темам {topics}: ошибки не должны быть вариациями одной причины. Сначала покажи только условие и код. Жди моего разбора, затем отдельно оцени найденные причины, последствия и исправления.",
    },
    {
        "id": "decision-lab",
        "title": "Архитектурная развилка",
        "description": "Выбери решение для трёх разных ситуаций и защити выбор через конкретные компромиссы.",
        "instruction": "Дай три непохожие backend-ситуации по темам {topics}: выбор подхода, ограничение или риск должны отличаться. В каждой предложи 2–3 правдоподобных варианта. Задавай ситуации по одной, проси выбрать и обосновать. Не повторяй один и тот же критерий другими словами. После всех трёх дай сравнительный разбор.",
    },
    {
        "id": "teach-back",
        "title": "Объясни как наставник",
        "description": "Объясни одну тему вслух простыми словами, затем исправь неточности по обратной связи.",
        "instruction": "Выбери одну из тем {topics}. Попроси меня объяснить её как начинающему разработчику за 5 минут. До ответа составь внутренний чек-лист: механизм, применение, ограничение и типичная ошибка. После ответа укажи только фактические пробелы. Задай не больше 3 уточнений, каждое по отдельному пункту чек-листа, без перефразирования уже заданного вопроса.",
    },
    {
        "id": "incident-drill",
        "title": "Учебный инцидент",
        "description": "Разбери поломку как разработчик: симптомы → гипотезы → проверка → исправление.",
        "instruction": "Придумай небольшой backend-инцидент, связанный с темами {topics}. Проверь, что симптомы и логи не противоречат задуманной причине. Дай только симптомы, логи и ограничения. Я должен построить гипотезы и план диагностики. Новые данные выдавай только в ответ на мои проверки, не задавая повторных наводящих вопросов, затем оцени ход расследования.",
    },
]


CAREER_ACTIONS = [
    {
        "id": "hh-scan",
        "title": "HH-разминка: срез требований",
        "description": "За 20 минут просмотри свежие junior Python/backend вакансии и выпиши три повторяющихся требования. По таймеру вернись к обучению.",
    },
    {
        "id": "hh-one-fit",
        "title": "HH-разминка: одно точное совпадение",
        "description": "Быстро проверь подходящие вакансии. Отправь не больше одного отклика только при хорошем совпадении; иначе просто зафиксируй недостающий навык.",
    },
    {
        "id": "hh-skill-signal",
        "title": "HH-разминка: сверка навыков",
        "description": "Сравни три свежие вакансии с текущей матрицей и отметь один общий пробел. Не перестраивай план по единичной вакансии.",
    },
]


# Границы включительные и относятся к позиции темы в TRACK_PRIORITY, а не к её
# историческому номеру. Этапы — волны, а не запреты: Django начинается на фоне
# позднего Python Core, а production и async идут параллельно после рабочего API.
ROADMAP_PHASES = [
    {
        "id": "foundation",
        "title": "Быстрый фундамент",
        "goal": "Основной Python и только необходимые стартовые части SQL, HTTP, тестирования, Git и Linux.",
        "milestone": "Писать небольшие программы и понимать базовый путь данных и запроса до начала Django.",
        "segments": [
            ("python", 1, 12),
            ("sql", 1, 4),
            ("http", 1, 4),
            ("testing", 1, 4),
            ("git", 1, 6),
            ("linux", 1, 6),
        ],
    },
    {
        "id": "backend-start",
        "title": "Python и первый Django параллельно",
        "goal": "Продолжать Python Core и одновременно применять SQL, HTTP, pytest и первые компоненты Django/Docker.",
        "milestone": "Собрать первые модели и API, понимая используемые конструкции Python и границы HTTP/БД.",
        "segments": [
            ("python", 13, 20),
            ("sql", 5, 12),
            ("http", 5, 12),
            ("testing", 5, 10),
            ("django", 1, 8),
            ("docker", 1, 4),
            ("git", 7, 12),
            ("linux", 7, 12),
        ],
    },
    {
        "id": "working-backend",
        "title": "Рабочий backend и завершение Python",
        "goal": "Закончить Python Core внутри практики Django, расширить SQL/HTTP и собрать тестируемый контейнеризованный сервис.",
        "milestone": "Рабочий Django API с БД, permissions, тестами, Docker Compose и воспроизводимым запуском.",
        "segments": [
            ("python", 21, 24),
            ("sql", 13, 18),
            ("http", 13, 18),
            ("testing", 11, 16),
            ("django", 9, 18),
            ("docker", 5, 16),
            ("git", 13, 16),
            ("linux", 13, 16),
        ],
    },
    {
        "id": "production-specialization",
        "title": "Production, Asyncio и отдельный трек алгоритмов",
        "goal": "После завершения Python Core подключить алгоритмы отдельным треком и параллельно закрыть production-темы и Asyncio/FastAPI.",
        "milestone": "Вся программа завершена: основной Django-стек, production-навыки и второй async-стек готовы к январскому поиску работы.",
        "segments": [
            ("sql", 19, 24),
            ("http", 19, 24),
            ("testing", 17, 24),
            ("django", 19, 24),
            ("docker", 17, 24),
            ("algorithms", 1, 24),
            ("git", 17, 24),
            ("linux", 17, 24),
            ("async", 1, 24),
        ],
    },
]


def parse_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def study_dates(count, start=START_DATE):
    current = parse_date(start)
    result = []
    while len(result) < count:
        if current.weekday() != 6:  # воскресенье — восстановление
            result.append(current)
        current += timedelta(days=1)
    return result


def phase_lanes(phase, tracks):
    """Возвращает очереди направлений этапа в dependency-first порядке."""
    lanes = []
    for track_id, first, last in phase["segments"]:
        track = tracks[track_id]
        topic_numbers = TRACK_PRIORITY[track_id][first - 1:last]
        lanes.append([(track, track["topics"][number - 1]) for number in topic_numbers])
    return lanes


def phase_groups(phase, tracks):
    """Плотно заполняет дни, не меняя порядок тем внутри направления."""
    lanes = phase_lanes(phase, tracks)
    positions = [0] * len(lanes)
    groups = []
    group_number = 0

    while any(position < len(lane) for position, lane in zip(positions, lanes)):
        current = []
        current_minutes = 0
        used_lanes = set()
        nonempty = [index for index, lane in enumerate(lanes) if positions[index] < len(lane)]
        leader = nonempty[group_number % len(nonempty)]

        while True:
            candidates = []
            for lane_index, lane in enumerate(lanes):
                if positions[lane_index] >= len(lane):
                    continue
                track, topic = lane[positions[lane_index]]
                minutes = sum(task["minutes"] for task in topic["tasks"]) + THEORY_MINUTES_PER_TOPIC
                if current_minutes + minutes <= LEARNING_MAX_MINUTES:
                    candidates.append((lane_index, track, topic, minutes))
            if not candidates:
                break
            if not current:
                selected = next(item for item in candidates if item[0] == leader)
            else:
                fresh = [item for item in candidates if item[0] not in used_lanes]
                selected = max(fresh or candidates, key=lambda item: (item[3], -item[0]))
            lane_index, track, topic, minutes = selected
            current.append((track, topic))
            current_minutes += minutes
            positions[lane_index] += 1
            used_lanes.add(lane_index)
            if current_minutes >= LEARNING_TARGET_MINUTES:
                break

        groups.append((phase, current, current_minutes))
        group_number += 1
    return groups


def daily_quest(day_number, phase, assigned, assigned_date):
    template = DAILY_QUESTS[(day_number - 1) % len(DAILY_QUESTS)]
    topic_names = ", ".join(topic["title"] for _track, topic in assigned) or "изученный Python, SQL, HTTP, Django, тесты и защита проекта"
    return {
        **template,
        "key": f'{assigned_date.isoformat()}-{template["id"]}',
        "minutes": REVIEW_MINUTES,
        "prompt": (
            f'Карьерный этап: {phase["title"]}.\n'
            + template["instruction"].format(topics=topic_names)
        ),
    }


def career_action(day_number, assigned_date):
    template = CAREER_ACTIONS[(day_number - 1) % len(CAREER_ACTIONS)]
    return {
        **template,
        "key": f'{assigned_date.isoformat()}-{template["id"]}',
        "minutes": CAREER_MINUTES,
    }


def build_daily_plan(start=START_DATE):
    tracks = {track["id"]: track for track in CURRICULUM}
    groups = []

    # Этапы не смешиваются. Поэтому milestone действительно означает, что весь
    # предыдущий слой знаний уже встретился в плане до следующего слоя.
    for phase in ROADMAP_PHASES:
        groups.extend(phase_groups(phase, tracks))

    dates = study_dates(len(groups), start)
    days = []
    for index, ((phase, assigned, learning_minutes), assigned_date) in enumerate(zip(groups, dates)):
        tasks = [task for _track, topic in assigned for task in topic["tasks"]]
        verification_minutes = VERIFICATION_MINUTES
        career_minutes = CAREER_MINUTES
        base_minutes = learning_minutes + verification_minutes + career_minutes
        consolidation_minutes = max(0, TARGET_MINUTES - base_minutes)
        days.append({
            "number": index + 1,
            "date": assigned_date,
            "phase": phase,
            "topics": assigned,
            "task_ids": [task["id"] for task in tasks],
            "minutes": base_minutes + consolidation_minutes,
            "learning_minutes": learning_minutes,
            "verification_minutes": verification_minutes,
            "career_minutes": career_minutes,
            "consolidation_minutes": consolidation_minutes,
            "review_minutes": REVIEW_MINUTES,
            "quest": daily_quest(index + 1, phase, assigned, assigned_date),
            "career_action": career_action(index + 1, assigned_date),
        })
    # По одному короткому воспроизведению материала через 1, 3, 7 и 14 учебных
    # дней. Интерфейс покажет только уже завершённые темы; незавершённые остаются
    # долгами и не маскируются под повторение.
    for index, day in enumerate(days):
        reviews = []
        for offset in (1, 3, 7, 14):
            source_index = index - offset
            if source_index < 0:
                continue
            source_topics = days[source_index]["topics"]
            if not source_topics:
                continue
            candidate = source_topics[(index + offset) % len(source_topics)]
            if candidate[1]["id"] not in {topic["id"] for _track, topic in reviews}:
                reviews.append(candidate)
        day["review_topics"] = reviews
    return days


def relevant_day(today=None, start=START_DATE):
    today = parse_date(today or date.today())
    plan = build_daily_plan(start)
    for day in plan:
        if day["date"] >= today:
            return day, day["date"] != today
    return plan[-1], True
