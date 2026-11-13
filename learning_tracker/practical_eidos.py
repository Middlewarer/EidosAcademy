"""Два проектных этапа Practical Eidos: самостоятельная песочница и интеграция."""


def _step(step_id, title, learn, build, evidence, requires=()):
    dependencies = f" После тем основной программы: {', '.join(requires)}." if requires else ""
    return (
        step_id,
        title,
        f"Изучить: {learn}. Реализовать самостоятельно: {build}. "
        f"Результат шага: {evidence}.{dependencies}",
    )


PRACTICAL_EIDOS_TRACKS = [
    {
        "id": "practical-sandbox",
        "title": "Practical Eidos · Этап 1. Самостоятельная песочница",
        "description": (
            "Отдельное красивое приложение с каталогом заданий, редактором, проверкой решения, "
            "историей попыток и собственным прогрессом. На этом этапе оно ещё не зависит от EidosAcademy."
        ),
        "counts_for_readiness": False,
        "milestones": [
            _step(
                "sandbox-foundation", "01 · Каркас приложения и дизайн-система",
                "структуру React-приложения, маршрутизацию, layout, design tokens, адаптивность и доступность",
                "создать отдельный проект Practical Eidos с главной, каталогом, страницей задания и профилем",
                "все четыре экрана связаны маршрутами, имеют единый визуальный язык и корректно работают на мобильном",
                ("http-02", "git-03", "git-04"),
            ),
            _step(
                "sandbox-domain", "02 · Модель задания",
                "моделирование Exercise, ExerciseVersion, TestCase, Tag, Track и связи между ними",
                "создать Django-модели, миграции и админку для публикации версионированных заданий",
                "из админки создаётся опубликованное задание с условием, сложностью, starter code и проверками",
                ("python-11", "sql-01", "django-02", "django-03", "django-12"),
            ),
            _step(
                "sandbox-api", "03 · API каталога и задания",
                "DRF serializers/ViewSets, filtering, pagination, validation и стабильную схему ошибок",
                "сделать API списка, фильтров, карточки задания и доступных вариантов окружения",
                "контракт воспроизводится через OpenAPI/curl и покрыт тестами валидного и ошибочного запросов",
                ("http-04", "http-06", "http-07", "http-10", "http-11", "django-06", "django-07", "django-15"),
            ),
            _step(
                "sandbox-auth", "04 · Пользователь и история попыток",
                "JWT-сессию, permissions, ownership и модели Submission/Attempt",
                "добавить регистрацию/вход и сохранение кода, статуса, времени, результата и номера попытки",
                "аноним не видит чужую историю, повторная отправка не создаёт случайный дубль",
                ("http-08", "django-08", "django-19", "testing-08"),
            ),
            _step(
                "sandbox-workspace", "05 · Рабочее место решения",
                "управление состоянием редактора, autosave, keyboard UX, loading/error/success и восстановление черновика",
                "собрать экран с условием, редактором, примерами, кнопкой запуска и панелью результата",
                "черновик не теряется при перезагрузке, интерфейс не прыгает между состояниями и доступен с клавиатуры",
                ("http-07", "testing-11"),
            ),
            _step(
                "sandbox-executor", "06 · Первый исполнитель задач",
                "для первого типа заданий — SQL, PGlite, WebAssembly, Web Worker, fixtures и reset окружения",
                "выполнять SQL ученика в отдельном worker на изолированном наборе данных",
                "запрос не блокирует интерфейс, окружение очищается между попытками, выполнение можно остановить",
                ("sql-02", "sql-03", "sql-04", "sql-08", "sql-09", "async-04"),
            ),
            _step(
                "sandbox-checker", "07 · Проверка и понятная обратная связь",
                "сравнение табличных результатов, типы/NULL/порядок, timeout и классификацию ошибок",
                "проверять результат, а не текст запроса, и показывать различия без раскрытия готового решения",
                "альтернативные корректные запросы принимаются, ошибка указывает на конкретное расхождение",
                ("testing-03", "testing-06", "testing-13", "http-22"),
            ),
            _step(
                "sandbox-beta", "08 · Прогресс, полировка и самостоятельная beta",
                "агрегацию прогресса, уровни сложности, E2E, CI, deployment и продуктовые события",
                "добавить solved/in-progress, счётчики, первый уровень экспертизы и выпустить 10 SQL-задач",
                "новый пользователь проходит путь каталог → задача → успешное решение → обновлённый профиль на production",
                ("sql-04", "testing-11", "testing-12", "git-22", "docker-21"),
            ),
        ],
    },
    {
        "id": "practical-integration",
        "title": "Practical Eidos · Этап 2. Интеграция с EidosAcademy",
        "description": (
            "Задания связываются с конкретными темами теоретического Eidos. Решение задачи передаёт "
            "доказательство практики, обновляет общий прогресс и уровень освоения темы."
        ),
        "counts_for_readiness": False,
        "milestones": [
            _step(
                "integration-contract", "09 · Контракт между двумя продуктами",
                "границы сервисов, source of truth, versioned API и contract testing",
                "зафиксировать, какие данные принадлежат EidosAcademy, какие Practical Eidos и какие события передаются",
                "есть схема взаимодействия и OpenAPI-контракт без прямого доступа одного приложения к БД другого",
                ("http-11", "http-24", "testing-14"),
            ),
            _step(
                "integration-identifiers", "10 · Стабильная связь урока и задания",
                "UUID/external_id, referential mapping и версионирование ссылок между сервисами",
                "дать Topic стабильный публичный идентификатор, а Exercise — theory_topic_id и версию связи",
                "перенос данных между dev/prod не ломает связь, удаление/архивация темы обработаны явно",
                ("django-02", "django-03", "sql-08", "sql-13"),
            ),
            _step(
                "integration-content", "11 · Задания внутри теоретического урока",
                "API-композицию, кеширование и graceful degradation внешней зависимости",
                "показывать в EidosAcademy связанные задания, сложность, статус и кнопку перехода в Practical Eidos",
                "урок работает при временной недоступности песочницы, а ссылка открывает правильное задание",
                ("http-10", "http-12", "django-12"),
            ),
            _step(
                "integration-identity", "12 · Единый пользователь и безопасный переход",
                "SSO, issuer/audience JWT, короткоживущий handoff token, CORS/CSRF и logout между приложениями",
                "сделать переход без повторной регистрации и безопасно сопоставить аккаунты двух систем",
                "токен нельзя переиспользовать или применить не к тому сервису, выход завершает связанную сессию",
                ("http-08", "http-09", "http-13", "django-24"),
            ),
            _step(
                "integration-events", "13 · Событие успешного решения",
                "webhooks/events, подпись запроса, idempotency, retry/backoff и transactional outbox",
                "после Accepted отправлять exercise.passed с user_id, topic_id, difficulty, attempt_id и временем",
                "повторная доставка не удваивает прогресс, временный сбой EidosAcademy восстанавливается автоматически",
                ("http-05", "http-12", "django-10", "django-18", "sql-09"),
            ),
            _step(
                "integration-mastery", "14 · Уровень освоения темы",
                "модель evidence-based mastery, веса сложности, хранение фактов отдельно от вычисленного уровня",
                "заменить один completed-флаг представлением theory_seen/practice_started/applied/confident",
                "уровень вычисляется из просмотров и успешных задач, причины каждого уровня видны пользователю",
                ("python-11", "sql-04", "django-09", "testing-13"),
            ),
            _step(
                "integration-reconcile", "15 · Сверка и восстановление прогресса",
                "eventual consistency, reconciliation job, audit log, observability и correlation ID",
                "добавить повторную сверку попыток и прогресса, админский просмотр ошибок синхронизации",
                "потерянное событие восстанавливается, расхождение диагностируется по одному correlation ID",
                ("http-23", "django-18", "django-21", "async-24"),
            ),
            _step(
                "integration-release", "16 · Сквозной релиз Theory + Practical",
                "E2E между приложениями, backward compatibility, feature flags, rollout и rollback",
                "выпустить один связанный SQL-модуль: теория, переход, решение, возврат и новый уровень экспертизы",
                "сквозной сценарий покрыт тестом и метриками, интеграцию можно отключить без поломки обоих продуктов",
                ("testing-11", "testing-14", "testing-24", "git-22", "docker-24"),
            ),
        ],
    },
]


def practical_eidos_projects():
    return [dict(track) for track in PRACTICAL_EIDOS_TRACKS]


def practical_step_count():
    return sum(len(track["milestones"]) for track in PRACTICAL_EIDOS_TRACKS)
