"""Конкретные кейсы и измеримые задания для всех 240 подтем."""

from __future__ import annotations

from expanded_topics import EXTRA_CASES


CASES = {
    "python": [
        "два имени ссылаются на один список progress, после append изменение видно через оба имени",
        "копия структуры course → modules → lessons должна независимо пережить изменение вложенного lesson",
        "для 100 000 course_id нужно выбрать коллекцию для поиска, уникальности и сохранения порядка",
        "каталог из 47 курсов разбивается на страницы по 9 элементов и поддерживает обратный просмотр",
        "функция create_course принимает обязательный title, keyword-only visibility и произвольные tags",
        "фабрика валидаторов создаётся в цикле для разных минимальных оценок и не должна захватывать последнее значение",
        "сырой JSON курсов преобразуется в словарь slug → число опубликованных уроков без нечитаемого comprehension",
        "ленивый объект перебирает строки журнала обучения один раз и корректно сообщает об исчерпании",
        "генератор читает 1 000 000 событий прогресса порциями и не собирает их все в память",
        "импорт курса различает ValidationError, FileNotFoundError и неизвестный сбой, сохраняя контекст в логах",
        "CourseCard моделируется dataclass, а разные источники курса реализуют единый Protocol",
        "сервис публикации разбит на типизированные модули и пишет структурированный лог с course_id и request_id",
    ],
    "sql": [
        "схема users, courses, enrollments и lessons должна запрещать потерянные связи и дубли записей",
        "из courses выбрать опубликованные записи после даты, отсортировать по рейтингу и корректно обработать NULL",
        "соединить users, enrollments и courses так, чтобы пользователь без записей не исчез из отчёта",
        "посчитать число студентов и средний прогресс по каждому курсу, оставив группы минимум с 10 студентами",
        "пронумеровать курсы внутри категории по популярности и вычислить накопительное число студентов",
        "через CTE получить дерево модулей, а затем отдельно отфильтровать курсы с общей длительностью более 5 часов",
        "подзапросом найти курсы выше среднего рейтинга своей категории и сравнить решение с JOIN",
        "нормализовать повторяющиеся данные автора и категории, сохранив контролируемый snapshot названия в заказе",
        "запись на курс и списание промокода выполняются атомарно при двух одновременных запросах",
        "подобрать индекс для списка опубликованных курсов по category_id и created_at без лишнего раздувания",
        "сравнить планы выборки прогресса до и после индекса на таблице в 500 000 строк",
        "устранить N+1 при выдаче 50 курсов с авторами и категориями, подтвердив число SQL-запросов",
    ],
    "http": [
        "проследить открытие учебного домена studyhub.local от DNS-запроса до TLS-handshake и первого HTTP-ответа",
        "разобрать запрос POST /api/courses с query, headers, JSON body и Content-Type",
        "выбрать GET, POST, PUT, PATCH или DELETE для публикации, замены и частичного изменения курса",
        "назначить корректные коды для создания курса, ошибки валидации, отсутствия, конфликта и сбоя upstream",
        "клиент повторяет запрос после 301, 302, 307 и 308, не теряя критичный метод и тело",
        "спроектировать ресурсы /courses, /enrollments и /progress без глаголов в URL и скрытых побочных эффектов",
        "версионировать изменение формата поля duration так, чтобы старый мобильный клиент продолжил работу",
        "сравнить cookie-session, JWT access/refresh и OAuth2 для входа студента и внешней интеграции",
        "React-клиент с другого origin вызывает DRF API с credentials и защищён от CSRF",
        "каталог использует ETag, Cache-Control, timeout и retry только для безопасных повторов",
        "описать API курсов в OpenAPI и воспроизвести положительный и ошибочный запрос через curl",
        "загрузка отчёта прогресса запускается повторно после timeout без двойного начисления результата",
    ],
    "django": [
        "разложить apps, settings, urls и зависимости учебного CourseService так, чтобы домены не образовали циклические импорты",
        "создать Course, Module и Lesson с ограничениями порядка, уникальным slug и осмысленными related_name",
        "изменить обязательность поля Course.level без потери существующих строк и с обратимой миграцией",
        "собрать QuerySet опубликованных курсов с фильтром, аннотацией students_count и стабильной сортировкой",
        "выдать каталог с category и modules без N+1, сравнив select_related и prefetch_related",
        "CourseSerializer проверяет диапазон price, согласованность дат и запрещённую смену owner",
        "выбрать ViewSet или APIView для CRUD курса и отдельной команды publish, не смешав бизнес-логику",
        "разрешить редактирование курса только владельцу или staff, а чтение — всем пользователям",
        "вынести enroll_user из serializer/view в сервис с явной транзакцией и доменной ошибкой",
        "публикация курса и создание первых материалов выполняются атомарно и устойчиво к повторному запросу",
        "загрузка обложки проверяет размер и тип, а secrets и окружения разделены через settings",
        "Django Admin показывает полезные фильтры, а кэш каталога инвалидируется после публикации курса",
    ],
    "testing": [
        "для расчёта прогресса определить наблюдаемое поведение, которое тест защищает от регрессии",
        "распределить проверки enroll_user между unit, integration и E2E без дублирования одного сценария",
        "применить equivalence partitioning и boundary values к рейтингу курса от 1 до 5",
        "написать pytest-тест чистой функции calculate_progress с понятной Arrange–Act–Assert структурой",
        "создать независимые fixtures user, course и enrollment с корректным scope и teardown",
        "одним parametrize проверить 8 комбинаций статуса курса и роли пользователя",
        "проверить транзакцию записи на курс через pytest-django, не оставляя данных между тестами",
        "через DRF APIClient проверить JWT-доступ, payload, статус и изменения в базе",
        "изолировать внешний email API через fake, а время — через mock без проверки внутренних вызовов ради вызовов",
        "проверить гонку двух записей на последнее место и доказать идемпотентность повторного запроса",
        "Playwright проходит путь каталог → карточка → избранное и сохраняет диагностический trace при сбое",
        "найти причину flaky-теста в CI и настроить coverage так, чтобы процент не заменял качество проверок",
    ],
    "git": [
        "проследить blob, tree и commit после изменения одного файла курса и объяснить роль HEAD",
        "показать различия working tree, index и repository на трёх версиях одного README",
        "разбить изменение API и документации на два атомарных commit с сообщениями, объясняющими причину",
        "создать feature-ветку курса, синхронизировать её и удалить после безопасного слияния",
        "слить две ветки с конфликтом в serializer и сохранить обе осмысленные части изменения",
        "перенести три локальных commit поверх обновлённого main через interactive rebase",
        "применить только commit с исправлением security-багa в release-ветку через cherry-pick",
        "отменить опубликованный commit через revert и восстановить потерянный локальный commit через reflog",
        "объяснить разницу fetch и pull, настроить upstream и безопасно обработать rejected push",
        "подготовить небольшой pull request с чек-листом, self-review и тремя содержательными review-комментариями",
        "создать аннотированный tag релиза и release notes из выбранных commit",
        "сравнить Gitflow и trunk-based для команды из пяти разработчиков с обязательным CI",
    ],
    "linux": [
        "найти конфигурацию учебного CourseService по абсолютному и относительному пути, не повредив символические ссылки",
        "создать сервисного пользователя и права на media так, чтобы процесс мог писать, а остальные — только читать",
        "найти в 2-гигабайтном логе строки ERROR по request_id через grep, find и безопасные шаблоны",
        "конвейером выделить десять самых частых HTTP-кодов без промежуточных файлов",
        "найти PID зависшего gunicorn, проверить ресурсы, отправить SIGTERM и только затем рассмотреть SIGKILL",
        "запустить management-команду с временной переменной окружения и объяснить наследование env",
        "диагностировать ситуацию: домен резолвится, но TCP-порт 443 недоступен из контейнера",
        "настроить SSH-ключ, known_hosts и безопасное подключение без передачи пароля",
        "создать systemd unit для backend с restart policy, WorkingDirectory и чтением environment file",
        "найти traceback одного request_id в journalctl и связать его с nginx access log",
        "определить причину заполненного диска и высокой памяти без немедленного удаления неизвестных файлов",
        "написать runbook для ответа 502: симптомы, команды, развилки решений и безопасный rollback",
    ],
    "docker": [
        "сравнить image и container на Python API и доказать, что удаление контейнера не удаляет образ",
        "написать минимальный Dockerfile для Django с непривилегированным пользователем и фиксированными зависимостями",
        "переставить COPY и install так, чтобы изменение исходника не пересобирало слой зависимостей",
        "настроить exec-form ENTRYPOINT, корректную передачу SIGTERM и отсутствие shell-процесса как PID 1",
        "разделить persistent PostgreSQL data, загруженные media и исходники разработки между volume и bind mount",
        "соединить backend и postgres по имени сервиса, не используя localhost внутри контейнера",
        "передать обычные настройки через env, а секрет БД не запечь в image и не вывести в git diff",
        "поднять backend, frontend, postgres и nginx через Compose с понятными зависимостями",
        "добавить healthcheck, который проверяет готовность API, а не только существование процесса",
        "выполнить migrations и collectstatic при деплое без параллельного запуска миграций каждым worker",
        "настроить nginx reverse proxy, статические файлы и TLS-терминацию для backend",
        "восстановить PostgreSQL из backup и собрать диагностический пакет логов после падения Compose",
    ],
    "async": [
        "сравнить конкурентную загрузку 30 API-ответов с параллельным CPU-расчётом рекомендаций",
        "показать момент создания coroutine и момент её выполнения event loop после await",
        "запустить 20 независимых запросов через create_task/gather и сохранить ошибки отдельных задач",
        "оборвать импорт курсов по timeout, корректно обработать CancelledError и освободить ресурсы",
        "обнаружить requests или time.sleep внутри async endpoint и измерить блокировку event loop",
        "получить данные из трёх внешних API через общий AsyncClient, лимит соединений и контролируемые retry",
        "спроектировать FastAPI routers для courses и enrollments с явными response models и status codes",
        "Pydantic-модель курса валидирует вложенные lessons, enum уровня и запрещает лишние поля",
        "вынести авторизацию и DB-session в Depends, не создавая скрытый глобальный state",
        "выполнить async-транзакцию SQLAlchemy и избежать ленивого I/O после закрытия session",
        "разделить endpoint, service, repository и Unit of Work для атомарной записи на курс",
        "выбрать BackgroundTasks, очередь или WebSocket для генерации отчёта и live-прогресса",
    ],
    "algorithms": [
        "оценить время и память удаления дублей из 1 000 000 course_id для list и set решений",
        "выбрать list, deque или связный список для истории последних действий и частых удалений с обоих концов",
        "за один проход посчитать уникальных студентов и частоты завершённых уроков через dict/set",
        "отсортировать курсы по сумме цифр в external_id, затем по title, не ломая стабильность",
        "найти course_id в отсортированном массиве и вернуть левую границу повторяющихся значений",
        "двумя указателями найти пару длительностей уроков с заданной суммой после сортировки",
        "найти самое длинное окно событий, содержащее не более трёх уникальных course_id",
        "проверить скобки в markdown-уроке через stack и обработать поток задач через queue",
        "сгенерировать все допустимые учебные планы из prerequisites с ранним отсечением невозможных веток",
        "обойти дерево категорий, вычислить глубину и вывести путь до заданного курса",
        "найти кратчайшую цепочку prerequisites через BFS и все достижимые зависимости через DFS",
        "через heap выбрать 10 самых популярных курсов из потока и обосновать жадный выбор",
    ],
}


PROFILES = {
    "python": ("Python", "solution.py + README.md", "py solution.py"),
    "sql": ("PostgreSQL", "schema.sql + solution.sql + result.txt", "psql -f schema.sql -f solution.sql"),
    "http": ("HTTP", "requests.http + answer.md", "все запросы воспроизводятся через curl или HTTP Client"),
    "django": ("Django/DRF", "models.py/views.py/serializers.py по условию + README.md", "py manage.py check"),
    "testing": ("pytest", "test_solution.py и минимальный тестируемый модуль", "py -m pytest -q"),
    "git": ("Git", "commands.txt + result.txt", "git status и git log подтверждают требуемое состояние"),
    "linux": ("Linux", "solution.sh + transcript.txt", "bash solution.sh завершается с кодом 0"),
    "docker": ("Docker", "Dockerfile/compose.yaml + verify.txt", "docker compose config и указанные проверки проходят"),
    "async": ("asyncio/FastAPI", "solution.py + README.md", "py solution.py или запуск FastAPI по команде из README"),
    "algorithms": ("Алгоритмы", "solution.py + README.md", "Accepted на LeetCode и локальный запуск примеров"),
}

LEETCODE_BY_TOPIC = {
    "Big O времени и памяти": ("contains-duplicate", "valid-anagram", "product-of-array-except-self"),
    "Массивы и строки": ("two-sum", "group-anagrams", "longest-substring-without-repeating-characters"),
    "Hash map и set": ("two-sum", "top-k-frequent-elements", "longest-consecutive-sequence"),
    "Сортировка и key": ("sort-an-array", "merge-intervals", "largest-number"),
    "Бинарный поиск": ("binary-search", "find-first-and-last-position-of-element-in-sorted-array", "search-in-rotated-sorted-array"),
    "Два указателя": ("valid-palindrome", "two-sum-ii-input-array-is-sorted", "3sum"),
    "Sliding window": ("best-time-to-buy-and-sell-stock", "longest-repeating-character-replacement", "minimum-window-substring"),
    "Stack и queue": ("valid-parentheses", "daily-temperatures", "largest-rectangle-in-histogram"),
    "Рекурсия и backtracking": ("subsets", "combination-sum", "n-queens"),
    "Деревья": ("maximum-depth-of-binary-tree", "binary-tree-level-order-traversal", "serialize-and-deserialize-binary-tree"),
    "Графы, BFS и DFS": ("number-of-islands", "clone-graph", "word-ladder"),
    "Heap и жадные алгоритмы": ("kth-largest-element-in-an-array", "task-scheduler", "merge-k-sorted-lists"),
    "Prefix sum": ("range-sum-query-immutable", "subarray-sum-equals-k", "continuous-subarray-sum"),
    "Интервалы": ("insert-interval", "merge-intervals", "non-overlapping-intervals"),
    "Linked list": ("reverse-linked-list", "linked-list-cycle", "merge-k-sorted-lists"),
    "Monotonic stack": ("next-greater-element-i", "daily-temperatures", "largest-rectangle-in-histogram"),
    "BST и balanced trees": ("validate-binary-search-tree", "kth-smallest-element-in-a-bst", "balance-a-binary-search-tree"),
    "Trie": ("implement-trie-prefix-tree", "design-add-and-search-words-data-structure", "word-search-ii"),
    "Union-Find": ("redundant-connection", "number-of-provinces", "min-cost-to-connect-all-points"),
    "Topological sort": ("course-schedule", "course-schedule-ii", "alien-dictionary"),
    "Dijkstra и взвешенные пути": ("network-delay-time", "path-with-minimum-effort", "cheapest-flights-within-k-stops"),
    "Dynamic programming": ("climbing-stairs", "coin-change", "longest-increasing-subsequence"),
    "Битовые операции": ("single-number", "counting-bits", "sum-of-two-integers"),
    "Строковые алгоритмы": ("find-the-index-of-the-first-occurrence-in-a-string", "repeated-substring-pattern", "shortest-palindrome"),
}

LEETCODE_MASTERY = {
    "Big O времени и памяти": ("maximum-subarray", "majority-element", "missing-number"),
    "Массивы и строки": ("container-with-most-water", "rotate-array", "spiral-matrix"),
    "Hash map и set": ("ransom-note", "isomorphic-strings", "word-pattern"),
    "Сортировка и key": ("sort-colors", "relative-sort-array", "maximum-gap"),
    "Бинарный поиск": ("search-a-2d-matrix", "find-minimum-in-rotated-sorted-array", "median-of-two-sorted-arrays"),
    "Два указателя": ("move-zeroes", "remove-duplicates-from-sorted-array", "trapping-rain-water"),
    "Sliding window": ("minimum-size-subarray-sum", "permutation-in-string", "sliding-window-maximum"),
    "Stack и queue": ("min-stack", "evaluate-reverse-polish-notation", "basic-calculator"),
    "Рекурсия и backtracking": ("permutations", "word-search", "palindrome-partitioning"),
    "Деревья": ("invert-binary-tree", "lowest-common-ancestor-of-a-binary-tree", "binary-tree-maximum-path-sum"),
    "Графы, BFS и DFS": ("max-area-of-island", "rotting-oranges", "surrounded-regions"),
    "Heap и жадные алгоритмы": ("last-stone-weight", "reorganize-string", "find-median-from-data-stream"),
    "Prefix sum": ("find-pivot-index", "range-sum-query-2d-immutable", "maximum-size-subarray-sum-equals-k"),
    "Интервалы": ("summary-ranges", "minimum-number-of-arrows-to-burst-balloons", "data-stream-as-disjoint-intervals"),
    "Linked list": ("middle-of-the-linked-list", "remove-nth-node-from-end-of-list", "reverse-nodes-in-k-group"),
    "Monotonic stack": ("remove-k-digits", "online-stock-span", "sum-of-subarray-minimums"),
    "BST и balanced trees": ("search-in-a-binary-search-tree", "convert-sorted-array-to-binary-search-tree", "recover-binary-search-tree"),
    "Trie": ("longest-common-prefix", "replace-words", "map-sum-pairs"),
    "Union-Find": ("satisfiability-of-equality-equations", "accounts-merge", "swim-in-rising-water"),
    "Topological sort": ("find-eventual-safe-states", "minimum-height-trees", "sort-items-by-groups-respecting-dependencies"),
    "Dijkstra и взвешенные пути": ("minimum-cost-to-make-at-least-one-valid-path-in-a-grid", "number-of-ways-to-arrive-at-destination", "find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance"),
    "Dynamic programming": ("house-robber", "unique-paths", "edit-distance"),
    "Битовые операции": ("number-of-1-bits", "reverse-bits", "maximum-xor-of-two-numbers-in-an-array"),
    "Строковые алгоритмы": ("longest-happy-prefix", "repeated-string-match", "minimum-window-substring"),
}


COMPLEXITY_TARGETS = {
    "Big O времени и памяти": "сначала добейтесь корректности, затем найдите решение за O(n) по времени",
    "Массивы и строки": "избегайте полного перебора пар; ориентир — O(n) или O(n log n)",
    "Hash map и set": "ориентир — O(n) по времени за счёт хеш-таблицы",
    "Сортировка и key": "ориентир — O(n log n); отдельно оцените память",
    "Бинарный поиск": "ориентир — O(log n)",
    "Два указателя": "после необходимой сортировки проход должен занимать O(n)",
    "Sliding window": "каждый элемент должен войти и выйти из окна не более одного раза: O(n)",
    "Stack и queue": "ориентир — O(n), без удаления из начала обычного list",
    "Рекурсия и backtracking": "оцените размер дерева перебора и добавьте раннее отсечение",
    "Деревья": "ориентир — O(n) по числу узлов; рекурсивная память O(h)",
    "Графы, BFS и DFS": "ориентир — O(V + E)",
    "Heap и жадные алгоритмы": "ориентир — O(n log k), если нужен только top-k",
    "Prefix sum": "подготовка O(n), один запрос диапазона O(1)",
    "Интервалы": "ориентир — O(n log n) из-за сортировки и O(n) на слияние",
    "Linked list": "ориентир — O(n) по времени и O(1) дополнительной памяти, где возможно",
    "Monotonic stack": "ориентир — O(n): каждый элемент кладётся и снимается не более одного раза",
    "BST и balanced trees": "объясните, когда операции O(log n), а когда деградируют до O(n)",
    "Trie": "ориентир операции — O(L), где L — длина строки",
    "Union-Find": "используйте path compression и union by rank/size; почти O(1) амортизированно",
    "Topological sort": "ориентир — O(V + E) с обязательной проверкой цикла",
    "Dijkstra и взвешенные пути": "ориентир — O((V + E) log V) с priority queue",
    "Dynamic programming": "сформулируйте состояние; не пересчитывайте одно состояние повторно",
    "Битовые операции": "ориентир — O(1) для фиксированной разрядности или O(log n) по числу битов",
    "Строковые алгоритмы": "для поиска подстроки стремитесь к O(n + m), а не O(n·m)",
}


SQL_PRACTICE = (
    "combine-two-tables", "employees-earning-more-than-their-managers", "duplicate-emails",
    "customers-who-never-order", "department-highest-salary", "delete-duplicate-emails",
    "rising-temperature", "game-play-analysis-i", "managers-with-at-least-5-direct-reports",
    "employee-bonus", "find-customer-referee", "customer-placing-the-largest-number-of-orders",
    "big-countries", "classes-more-than-5-students", "sales-person", "tree-node",
    "biggest-single-number", "not-boring-movies", "exchange-seats", "swap-salary",
    "customers-who-bought-all-products", "product-sales-analysis-iii",
    "product-price-at-a-given-date", "last-person-to-fit-in-the-bus",
)


OPTIONAL_PRACTICE = {
    ("python", 3): [
        ("Contains Duplicate", "easy", "выбрать set для проверки уникальности за O(n)", "contains-duplicate"),
        ("Two Sum", "easy", "использовать dict для поиска дополнения за O(n)", "two-sum"),
    ],
    ("python", 4): [
        ("Reverse String", "easy", "применить два указателя и работу с индексами", "reverse-string"),
        ("Rotate Array", "medium", "отработать срезы или развороты без квадратичного алгоритма", "rotate-array"),
    ],
    ("python", 7): [
        ("Group Anagrams", "medium", "построить читаемую группировку через dict", "group-anagrams"),
        ("Top K Frequent Elements", "medium", "посчитать частоты и выбрать top-k", "top-k-frequent-elements"),
    ],
    ("python", 8): [
        ("Flatten Nested List Iterator", "medium", "реализовать ленивый обход вложенной структуры", "flatten-nested-list-iterator"),
        ("Peeking Iterator", "medium", "добавить peek поверх протокола iterator", "peeking-iterator"),
    ],
    ("sql", 2): [
        ("Big Countries", "easy", "закрепить WHERE и логические условия", "big-countries"),
        ("Find Customer Referee", "easy", "корректно обработать NULL в фильтрации", "find-customer-referee"),
    ],
    ("sql", 3): [
        ("Combine Two Tables", "easy", "выбрать LEFT JOIN и сохранить строки без совпадения", "combine-two-tables"),
        ("Employee Bonus", "easy", "соединить таблицы и отфильтровать nullable-значения", "employee-bonus"),
    ],
    ("sql", 4): [
        ("Duplicate Emails", "easy", "использовать GROUP BY и HAVING", "duplicate-emails"),
        ("Classes More Than 5 Students", "easy", "посчитать уникальных участников группы", "classes-more-than-5-students"),
    ],
    ("sql", 5): [
        ("Customers Who Never Order", "easy", "сравнить NOT EXISTS и anti-join", "customers-who-never-order"),
        ("Employees Earning More Than Their Managers", "easy", "применить self-join или подзапрос", "employees-earning-more-than-their-managers"),
    ],
}


def topic_practice_links(track_id, topic_index):
    """Необязательные алгоритмические задачи, не влияющие на прогресс темы."""
    return [
        {
            "title": title,
            "difficulty": difficulty,
            "target": target,
            "url": f"https://leetcode.com/problems/{slug}/",
        }
        for title, difficulty, target, slug in OPTIONAL_PRACTICE.get((track_id, topic_index), [])
    ]


PRACTICE_INTRO = {
    "python": "Напишите на Python небольшую запускаемую программу. Условие",
    "sql": "Создайте минимальные таблицы и тестовые строки, затем напишите SQL, решающий задачу. Условие",
    "django": "В минимальном Django-приложении напишите только код, необходимый для решения задачи. Условие",
    "testing": "Напишите небольшой pytest-модуль, который проверяет указанное поведение. Условие",
    "async": "Напишите запускаемую асинхронную программу на Python. Условие",
}


PRACTICE_RESULT = {
    "python": "Короткий код решения и два обычных assert, проверяющих основное поведение и один крайний случай.",
    "sql": "SQL-файл со схемой, тестовыми данными и итоговым запросом; ниже — фактический результат запроса.",
    "django": "Изменённые Python-файлы и одна команда, которой можно проверить, что код загружается без ошибок.",
    "testing": "Тестовый модуль и вывод одного запуска pytest.",
    "async": "Код решения и фактический вывод запуска; программа должна завершаться сама.",
}


# One deliberately chosen interview task per algorithmic pattern.  Keep these
# keyed by topic title so task IDs remain stable when the wording is improved.
ALGORITHM_CHALLENGES = {
    "Big O времени и памяти": {
        "title": "Первый повтор в потоке идентификаторов",
        "slug": "contains-duplicate", "difficulty": "medium", "minutes": 35,
        "statement": (
            "Дан список course_ids длиной до 1 000 000. Верните первый идентификатор, который встретился повторно "
            "при просмотре слева направо, и индекс его второго появления; если повторов нет — (None, -1). "
            "Пример: [42, 7, 19, 7, 42] → (7, 3). Сначала письменно оцените решение с вложенным поиском, "
            "затем реализуйте один проход. Не сортируйте вход и не изменяйте его. Цель: O(n) времени и O(n) памяти."
        ),
    },
    "Массивы и строки": {
        "title": "Сгруппировать анаграммы",
        "slug": "group-anagrams", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Сгруппируйте слова, состоящие из строчных латинских букв, по анаграммам. Порядок групп не важен, "
            "но порядок слов внутри группы сохраните как во входе. Пример: [\"eat\", \"tea\", \"tan\", \"ate\", \"nat\"] "
            "→ [[\"eat\", \"tea\", \"ate\"], [\"tan\", \"nat\"]]. Не сравнивайте каждую пару слов. "
            "Объясните два ключа группы — сортированную строку и частоты букв — и выберите один."
        ),
    },
    "Hash map и set": {
        "title": "Самая длинная последовательность без сортировки",
        "slug": "longest-consecutive-sequence", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Для неотсортированного массива целых чисел найдите длину самой длинной последовательности соседних "
            "значений. Пример: [100, 4, 200, 1, 3, 2, 2] → 4 для 1,2,3,4. Сортировать нельзя. "
            "Начинайте расширение только с числа, у которого нет предшественника. Цель: O(n) среднего времени; "
            "отдельно объясните, почему каждое уникальное число посещается ограниченное число раз."
        ),
    },
    "Сортировка и key": {
        "title": "Объединить интервалы встреч",
        "slug": "merge-intervals", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Даны интервалы занятости [start, end]. Объедините все пересекающиеся и соприкасающиеся интервалы. "
            "Пример: [[1,3],[2,6],[8,10],[10,12],[15,18]] → [[1,6],[8,12],[15,18]]. "
            "Вход может быть не отсортирован. Сформулируйте ключ сортировки и инвариант уже собранного результата. "
            "Цель: O(n log n) времени; исходный список изменять нельзя."
        ),
    },
    "Бинарный поиск": {
        "title": "Поиск в циклически сдвинутом массиве",
        "slug": "search-in-rotated-sorted-array", "difficulty": "medium", "minutes": 50,
        "statement": (
            "В массиве уникальных чисел, полученном циклическим сдвигом отсортированного массива, найдите индекс target. "
            "Пример: nums=[4,5,6,7,0,1,2], target=0 → 4; target=3 → -1. На каждой итерации явно определяйте, "
            "какая половина отсортирована, и отбрасывайте только ту часть, где target точно отсутствует. "
            "Цель: O(log n); добавьте тесты для сдвига на 0, одного элемента и target на границе."
        ),
    },
    "Два указателя": {
        "title": "Найти все уникальные тройки с нулевой суммой",
        "slug": "3sum", "difficulty": "medium", "minutes": 55,
        "statement": (
            "Верните все уникальные тройки значений с суммой 0. Пример: [-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]. "
            "После сортировки фиксируйте первый элемент и двигайте два указателя; не используйте множество готовых "
            "троек как замену корректной обработке дублей. Цель: O(n²) времени. Объясните, почему O(n³) не нужен."
        ),
    },
    "Sliding window": {
        "title": "Самая длинная подстрока без повторов",
        "slug": "longest-substring-without-repeating-characters", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Найдите длину самой длинной подстроки без повторяющихся символов. Пример: \"abba\" → 2, \"pwwkew\" → 3. "
            "Храните последнюю позицию символа и никогда не сдвигайте левую границу назад. Цель: O(n) времени. "
            "Добавьте тесты для пустой строки, одинаковых символов и случая, где повтор находится левее текущего окна."
        ),
    },
    "Stack и queue": {
        "title": "Сколько ждать более тёплого дня",
        "slug": "daily-temperatures", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Для каждого значения температуры верните число дней до следующей более высокой температуры, иначе 0. "
            "Пример: [73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]. Используйте монотонный стек индексов, "
            "а не вложенный поиск. Цель: O(n). На бумаге покажите состояние стека после каждого из первых пяти элементов."
        ),
    },
    "Рекурсия и backtracking": {
        "title": "Комбинации чисел с заданной суммой",
        "slug": "combination-sum", "difficulty": "medium", "minutes": 55,
        "statement": (
            "Даны уникальные положительные candidates и target. Верните все комбинации, дающие target; число можно "
            "использовать повторно. Пример: [2,3,6,7], 7 → [[2,2,3],[7]]. Постройте дерево выбора, передавайте индекс "
            "начала и прекращайте ветку, когда остаток отрицателен. Не создавайте перестановки одной комбинации."
        ),
    },
    "Деревья": {
        "title": "Обход дерева по уровням",
        "slug": "binary-tree-level-order-traversal", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Верните значения бинарного дерева по уровням: [3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]. "
            "Используйте deque и фиксируйте длину очереди в начале каждого уровня. Цель: O(n) времени и O(w) памяти, "
            "где w — максимальная ширина. Проверьте пустое дерево и вырожденное дерево из одной ветви."
        ),
    },
    "Графы, BFS и DFS": {
        "title": "Посчитать острова в сетке",
        "slug": "number-of-islands", "difficulty": "medium", "minutes": 50,
        "statement": (
            "В прямоугольной сетке из '1' и '0' посчитайте компоненты суши, соединённые по четырём направлениям. "
            "Пример: [[1,1,0],[0,1,0],[1,0,1]] → 3. Для каждой новой компоненты запускайте BFS или DFS и отмечайте "
            "клетку посещённой до добавления соседей. Цель: O(rows·cols); не используйте рекурсию без оценки глубины."
        ),
    },
    "Heap и жадные алгоритмы": {
        "title": "K самых частых элементов",
        "slug": "top-k-frequent-elements", "difficulty": "medium", "minutes": 50,
        "statement": (
            "Верните k наиболее частых чисел. Пример: [1,1,1,2,2,3], k=2 → [1,2]. Реализуйте решение через "
            "частоты и heap размера k; сравните его с bucket-подходом. Цель heap-версии: O(n log k), а не сортировка "
            "всех уникальных значений. Опишите поведение при равных частотах."
        ),
    },
    "Prefix sum": {
        "title": "Количество подмассивов с суммой k",
        "slug": "subarray-sum-equals-k", "difficulty": "medium", "minutes": 50,
        "statement": (
            "Посчитайте непрерывные подмассивы с суммой k. Пример: nums=[1,1,1], k=2 → 2; [1,-1,0], k=0 → 3. "
            "Храните количество ранее встреченных префиксных сумм и начните с частоты {0: 1}. Скользящее окно "
            "не подходит из-за отрицательных чисел. Цель: O(n) времени и O(n) памяти."
        ),
    },
    "Интервалы": {
        "title": "Вставить новый интервал",
        "slug": "insert-interval", "difficulty": "medium", "minutes": 45,
        "statement": (
            "В отсортированный непересекающийся список интервалов вставьте newInterval и объедините пересечения. "
            "Пример: [[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8] → [[1,2],[3,10],[12,16]]. "
            "Сделайте три явные фазы: интервалы слева, слияние, интервалы справа. Цель: O(n) без повторной сортировки."
        ),
    },
    "Linked list": {
        "title": "Найти начало цикла в связном списке",
        "slug": "linked-list-cycle-ii", "difficulty": "medium", "minutes": 55,
        "statement": (
            "Верните узел, в котором начинается цикл, либо None. Используйте медленный и быстрый указатели без set. "
            "После встречи перенесите один указатель в head и двигайте оба по одному шагу. Цель: O(n) времени и O(1) "
            "памяти. Отдельно докажите, почему вторая встреча происходит именно на входе в цикл."
        ),
    },
    "Monotonic stack": {
        "title": "Максимальный прямоугольник в гистограмме",
        "slug": "largest-rectangle-in-histogram", "difficulty": "hard", "minutes": 70,
        "statement": (
            "Для heights найдите максимальную площадь прямоугольника. Пример: [2,1,5,6,2,3] → 10. Храните в "
            "монотонном стеке пары (start_index, height); при меньшей высоте закрывайте все более высокие столбцы и "
            "переносите их начало. Добавьте нулевой sentinel. Цель: O(n), каждый столбец входит и выходит один раз."
        ),
    },
    "BST и balanced trees": {
        "title": "Проверить корректность BST",
        "slug": "validate-binary-search-tree", "difficulty": "medium", "minutes": 45,
        "statement": (
            "Проверьте, является ли бинарное дерево BST. Ограничение предка действует на всё поддерево: пример "
            "[5,1,4,null,null,3,6] должен вернуть false. Передавайте допустимый открытый диапазон (low, high); "
            "дубликаты считайте ошибкой. Цель: O(n) времени и O(h) памяти."
        ),
    },
    "Trie": {
        "title": "Реализовать префиксное дерево",
        "slug": "implement-trie-prefix-tree", "difficulty": "medium", "minutes": 60,
        "statement": (
            "Реализуйте Trie с insert(word), search(word) и starts_with(prefix). После insert('apple'): search('app') "
            "false, starts_with('app') true; после insert('app') search('app') true. Не путайте конец слова с наличием "
            "префикса. Цель каждой операции: O(L). Добавьте тест на пустой префикс и общие ветви слов."
        ),
    },
    "Union-Find": {
        "title": "Объединить аккаунты по общим email",
        "slug": "accounts-merge", "difficulty": "medium", "minutes": 70,
        "statement": (
            "Объедините записи аккаунтов, если они имеют хотя бы один общий email, включая транзитивные связи. "
            "Примените DSU с path compression и union by size/rank, затем соберите email по корню. Email в результате "
            "отсортируйте. Объясните, почему попарного сравнения аккаунтов недостаточно и какова сложность решения."
        ),
    },
    "Topological sort": {
        "title": "Построить порядок прохождения курсов",
        "slug": "course-schedule-ii", "difficulty": "medium", "minutes": 55,
        "statement": (
            "Для num_courses и пар [course, prerequisite] верните любой допустимый порядок или [] при цикле. "
            "Пример: 4, [[1,0],[2,0],[3,1],[3,2]] → [0,1,2,3] или [0,2,1,3]. Реализуйте алгоритм Кана: "
            "indegree, очередь нулевых степеней, подсчёт обработанных вершин. Цель: O(V+E)."
        ),
    },
    "Dijkstra и взвешенные пути": {
        "title": "Время распространения сигнала по сети",
        "slug": "network-delay-time", "difficulty": "medium", "minutes": 60,
        "statement": (
            "Дан ориентированный граф times=[u,v,w], n вершин и старт k. Верните время, за которое сигнал достигнет "
            "всех вершин, либо -1. Используйте список смежности и min-heap; устаревшие записи heap пропускайте. "
            "Цель: O((V+E) log V). Добавьте недостижимую вершину и объясните, почему отрицательные веса запрещены."
        ),
    },
    "Dynamic programming": {
        "title": "Минимальное число монет",
        "slug": "coin-change", "difficulty": "medium", "minutes": 60,
        "statement": (
            "Для coins и amount верните минимальное число монет или -1. Пример: [1,2,5], 11 → 3; [2], 3 → -1. "
            "До кода сформулируйте состояние dp[x], базу и переход. Реализуйте bottom-up без повторного пересчёта "
            "состояний. Цель: O(amount·len(coins)) времени и O(amount) памяти."
        ),
    },
    "Битовые операции": {
        "title": "Число единичных битов от 0 до n",
        "slug": "counting-bits", "difficulty": "medium", "minutes": 40,
        "statement": (
            "Верните ans, где ans[i] — число единичных битов i для всех 0≤i≤n. Пример: n=5 → [0,1,1,2,1,2]. "
            "Не вызывайте bin и не пересчитывайте каждый бит с нуля. Используйте зависимость dp[i] от i>>1 или "
            "i&(i-1). Цель: O(n) времени. Объясните обе формулы на двоичном примере 6 (110)."
        ),
    },
    "Строковые алгоритмы": {
        "title": "Найти подстроку алгоритмом KMP",
        "slug": "find-the-index-of-the-first-occurrence-in-a-string", "difficulty": "hard", "minutes": 75,
        "statement": (
            "Реализуйте поиск первого вхождения needle в haystack без str.find, срезов для каждого старта и regex. "
            "Постройте prefix/LPS-массив и используйте его при несовпадении. Пример: haystack='ababcabcabababd', "
            "needle='ababd' → 10. Цель: O(n+m). Покажите LPS для 'ababaca' и тесты для пустой строки и перекрытий."
        ),
    },
}


def build_unique_tasks(track_id, topic_id, topic_title, theory, pitfall, artifact, topic_index):
    """Даёт только полезные для темы задания, без искусственного заполнения квоты."""
    cases = CASES[track_id] + EXTRA_CASES[track_id]
    case = cases[topic_index - 1]
    _environment, _files, run_check = PROFILES[track_id]
    specs = [{
        "kind": "theory", "difficulty": "easy", "minutes": 10,
        "label": "ТЕОРИЯ", "tab_label": "Теория",
        "title": f"{topic_title}: объяснение своими словами",
        "statement": (
            f"В 2–4 предложениях объясните тему «{topic_title}» своими словами: как она работает, "
            f"когда нужна и почему опасна ошибка «{pitfall}». При необходимости добавьте один короткий пример."
        ),
        "deliverable": "Ответ можно написать прямо в приложении. Вы сами решаете, достаточно ли хорошо поняли тему.",
        "example": "Связный ответ без пересказа определения из документации.",
    }]

    if track_id in PRACTICE_INTRO:
        specs.append({
            "kind": "code", "difficulty": "medium", "minutes": 25,
            "label": "КОД", "tab_label": "Код",
            "title": f"{topic_title}: практическая задача",
            "statement": f"{PRACTICE_INTRO[track_id]}: {case}.",
            "deliverable": PRACTICE_RESULT[track_id],
            "example": f"Рекомендуемая команда проверки: {run_check}.",
        })

    if track_id == "algorithms":
        # Preserve the legacy IDs while making each topic a real skill check.
        challenge = ALGORITHM_CHALLENGES[topic_title]
        specs[0]["id"] = f"{topic_id}-p06"
        specs[0].update({
            "difficulty": "medium", "minutes": 15,
            "label": "РАЗБОР", "tab_label": "Разбор подхода",
            "title": f"{topic_title}: объяснить решение до кода",
            "statement": (
                f"До практики по теме «{topic_title}» письменно зафиксируйте: 1) brute force и его сложность; "
                "2) признак, по которому узнаётся нужный паттерн; 3) инвариант оптимального решения; "
                f"4) два крайних случая. Отдельно объясните, как избежать ошибки «{pitfall}»."
            ),
            "deliverable": (
                "Короткий разбор из четырёх пунктов. Если вы не можете сформулировать инвариант без кода, "
                "тема ещё не готова к практике."
            ),
            "example": "Не переписывайте теорию: объясните ход решения так, как объясняли бы интервьюеру.",
        })
        specs.append({
            "id": f"{topic_id}-p01",
            "kind": "code", "difficulty": challenge["difficulty"], "minutes": challenge["minutes"],
            "label": "ЗАДАЧА", "tab_label": "Задача на владение",
            "title": challenge["title"],
            "statement": challenge["statement"],
            "deliverable": (
                "solution.py без подсказок; минимум 5 assert-тестов, включая названные крайние случаи; "
                "в README — инвариант, доказательство корректности и точная оценка времени/памяти. "
                "Отмечайте выполненным только после повторного решения с чистого листа."
            ),
            "example": f"Контроль сложности: {COMPLEXITY_TARGETS[topic_title]}.",
            "external_url": f"https://leetcode.com/problems/{challenge['slug']}/",
        })
    tasks = []
    for index, spec in enumerate(specs, 1):
        item = {
            "id": spec.get("id", f"{topic_id}-p{index:02d}"),
            "title": spec["title"],
            "label": spec["label"],
            "tab_label": spec["tab_label"],
            "kind": spec["kind"],
            "description": spec["statement"],
            "statement": spec["statement"],
            "deliverable": spec["deliverable"],
            "example": spec["example"],
            "constraints": [],
            "checks": [],
            "acceptance": "",
            "difficulty": spec["difficulty"],
            "minutes": spec["minutes"],
            "steps": [],
            "case": case,
            "artifact": artifact,
        }
        if spec.get("external_url"):
            item["external_url"] = spec["external_url"]
            item["external_label"] = "Открыть связанную задачу на LeetCode"
        tasks.append(item)
    return tasks
