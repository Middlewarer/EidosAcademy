"""Build the Anki deck for every tracker topic scheduled through 2026-10-10."""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

import genanki


ROOT = Path(__file__).resolve().parents[2]
TRACKER = ROOT / "learning_tracker"
OUTPUT = Path(__file__).resolve().parent / "output"
DEADLINE = date(2026, 10, 10)
STATE = Path.home() / ".eidos_learning_tracker" / "progress.json"

sys.path.insert(0, str(TRACKER))
from daily_plan import build_daily_plan  # noqa: E402
from concrete_expansion import EXTRA_CONCRETE  # noqa: E402


MODEL_ID = 1607392319
MODEL = genanki.Model(
    MODEL_ID,
    "Eidos Mastery RU",
    fields=[
        {"name": "ID"},
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "Context"},
        {"name": "Source"},
    ],
    templates=[{
        "name": "Recall",
        "qfmt": '<div class="meta">{{Context}}</div><div class="question">{{Question}}</div>',
        "afmt": '{{FrontSide}}<hr id="answer"><div class="answer">{{Answer}}</div><div class="source">{{Source}}</div>',
    }],
    css="""
.card { font-family: Arial, sans-serif; font-size: 19px; line-height: 1.45;
        text-align: left; color: #e8edf7; background: #111827; padding: 18px; }
.meta { color: #8bb8ff; font-size: 13px; text-transform: uppercase; margin-bottom: 14px; }
.question { font-size: 21px; font-weight: 650; }
.answer { margin-top: 16px; }
.source { margin-top: 20px; color: #8a96aa; font-size: 12px; }
pre { white-space: pre-wrap; background: #0b1020; border: 1px solid #29344d;
      border-radius: 8px; padding: 12px; overflow-wrap: anywhere; }
code { font-family: Consolas, monospace; color: #d7e6ff; }
hr { border: 0; border-top: 1px solid #334155; margin: 22px 0; }
""",
)


PYTHON_DEEP = {
    "python-01": [
        ("Что выведет код?<pre><code>a = []\nb = a\nb.append(1)\nprint(a, a is b)</code></pre>", "<code>[1] True</code>. Оба имени ссылаются на один объект; append изменяет этот объект."),
        ("Когда в Python уместен <code>is</code>?", "Для проверки идентичности, прежде всего <code>x is None</code>. Значения строк, чисел и коллекций обычно сравнивают через <code>==</code>."),
        ("Может ли <code>a == b</code> быть True, а <code>a is b</code> — False?", "Да. Два разных объекта могут быть равны по значению, например два отдельно созданных списка <code>[1]</code>."),
    ],
    "python-02": [
        ("Что не копирует <code>list.copy()</code>?", "Вложенные объекты. Создаётся новый внешний список, но его элементы остаются теми же ссылками."),
        ("Когда нужен <code>copy.deepcopy()</code>?", "Когда требуется рекурсивно отделить изменяемое вложенное состояние. Использовать автоматически не стоит: это дороже и не для всех объектов осмысленно."),
        ("Почему изменение immutable-объекта не меняет его на месте?", "Операция создаёт новый объект и переназначает имя; исходный объект остаётся прежним."),
    ],
    "python-03": [
        ("Какую коллекцию выбрать для быстрой проверки принадлежности уникальных hashable-значений?", "<code>set</code>: средняя проверка принадлежности — O(1), порядок доступа по индексу не поддерживается."),
        ("Что требуется от ключа <code>dict</code>?", "Он должен быть hashable: иметь стабильный hash и согласованное сравнение равенства за время нахождения в словаре."),
        ("Когда tuple лучше list?", "Когда последовательность логически фиксирована, должна быть неизменяемой или использоваться как ключ при условии hashable-элементов."),
    ],
    "python-04": [
        ("Какие границы использует срез <code>seq[start:stop]</code>?", "Полуинтервал: start включён, stop исключён. Это удобно для длины <code>stop-start</code>."),
        ("Что означает <code>seq[::-1]</code>?", "Создать обращённую поверхностную копию последовательности с шагом −1."),
        ("Что делает <code>first, *middle, last = values</code>?", "Распаковывает первый и последний элементы, а все промежуточные собирает в новый список <code>middle</code>."),
    ],
    "python-05": [
        ("Почему опасен аргумент <code>items=[]</code> по умолчанию?", "Объект создаётся один раз при определении функции и переиспользуется между вызовами. Обычно используют <code>None</code> и создают список внутри."),
        ("Что разделяет символ <code>/</code> в сигнатуре функции?", "Параметры слева от <code>/</code> можно передавать только позиционно."),
        ("Что разделяет одиночный <code>*</code> в сигнатуре?", "Параметры справа от него становятся keyword-only и должны передаваться по имени."),
    ],
    "python-06": [
        ("Каков порядок поиска имени по LEGB?", "Local → Enclosing → Global → Builtins."),
        ("Почему lambda в цикле часто видит последнее значение переменной?", "Замыкание захватывает имя, а не снимок его значения; значение ищется при вызове. Зафиксировать можно аргументом по умолчанию."),
        ("Чем отличаются <code>global</code> и <code>nonlocal</code>?", "<code>global</code> связывает имя с модулем, <code>nonlocal</code> — с ближайшей enclosing-областью функции."),
    ],
    "python-07": [
        ("Когда comprehension лучше заменить обычным циклом?", "Когда есть несколько уровней условий, побочные эффекты, сложное ветвление или логика перестаёт читаться с первого взгляда."),
        ("Чем generator expression отличается от list comprehension?", "Генератор вычисляет элементы лениво и одноразово; list comprehension сразу материализует весь список."),
        ("Допустимы ли побочные эффекты внутри comprehension?", "Технически возможны, но обычно ухудшают ясность. Comprehension лучше использовать для преобразования и фильтрации значений."),
    ],
    "python-08": [
        ("Чем iterable отличается от iterator?", "Iterable умеет вернуть iterator через <code>iter()</code>; iterator хранит состояние обхода и возвращает себя из <code>iter()</code>."),
        ("Что сигнализирует конец итерации?", "Исключение <code>StopIteration</code> из <code>__next__</code>; цикл <code>for</code> обрабатывает его сам."),
        ("Почему второй проход по iterator может быть пустым?", "Iterator обычно одноразовый и уже исчерпан. Для повторного прохода нужен новый iterator или материализованная коллекция."),
    ],
    "python-10": [
        ("Почему <code>except Exception: pass</code> опасен?", "Он скрывает причину, оставляет программу в непонятном состоянии и лишает диагностики. Ловят ожидаемые исключения и обрабатывают их явно."),
        ("Для чего служит <code>else</code> у <code>try</code>?", "Блок выполняется, только если в <code>try</code> не было исключения; туда выносят код, который не нужно покрывать обработчиком."),
        ("Выполнится ли <code>finally</code> при <code>return</code>?", "Да, перед фактическим выходом из функции. Редкие аварийные завершения процесса являются исключением из обычной модели."),
    ],
    "python-11": [
        ("Когда <code>@dataclass</code> особенно уместен?", "Для классов, основная роль которых — хранить структурированные данные; он генерирует типовой init/repr/eq по объявленным полям."),
        ("Чем Protocol отличается от обычного наследования интерфейса?", "Protocol поддерживает структурную типизацию: объект подходит по набору методов и атрибутов без явного наследования."),
        ("Почему композиция часто безопаснее наследования?", "Она уменьшает связанность и не требует соблюдать неочевидный контракт базового класса; поведение можно заменять явно."),
    ],
    "python-12": [
        ("Проверяет ли Python type hints во время выполнения автоматически?", "Нет. Аннотации описывают контракт для людей и инструментов; runtime-проверка требует отдельного кода или библиотеки."),
        ("Почему logging лучше случайных print в backend?", "Он даёт уровни, структурированный контекст, обработчики и централизованную настройку без смешивания диагностики с обычным выводом."),
        ("Что защищает конструкция <code>if __name__ == '__main__'</code>?", "Не даёт запускать CLI/демо-код при импорте модуля; при прямом запуске модуля условие истинно."),
    ],
    "python-19": [
        ("Что изолирует virtual environment?", "Python-интерпретатор/пути и установленные пакеты проекта; системные библиотеки ОС он не контейнеризирует."),
        ("Зачем фиксировать разрешённые версии зависимостей?", "Чтобы одинаковые исходники воспроизводимо собирались сегодня, в CI и у другого разработчика."),
        ("Какова роль <code>pyproject.toml</code>?", "Единое место для build-system, метаданных проекта, зависимостей и конфигурации поддерживающих инструментов."),
    ],
    "python-20": [
        ("Почему путь относительно текущей директории хрупок?", "Рабочая директория задаётся способом запуска и может отличаться от каталога модуля. Базовый путь нужно выбирать явно."),
        ("Зачем открывать текстовый файл с явной <code>encoding='utf-8'</code>?", "Чтобы результат не зависел от системной кодировки и одинаково работал на разных машинах."),
        ("Что гарантирует <code>with open(...) as f</code>?", "Файл будет закрыт при нормальном выходе и при исключении внутри блока."),
    ],
    "python-21": [
        ("Почему <code>float</code> не подходит для точных денежных расчётов?", "Двоичное представление не может точно хранить многие десятичные дроби. Используют <code>Decimal</code> с явными правилами округления."),
        ("Что такое timezone-aware datetime?", "Объект с информацией о часовом смещении/зоне; он позволяет однозначнее сравнивать и преобразовывать моменты времени."),
        ("Почему <code>json.dumps()</code> не сериализует Decimal и datetime по умолчанию?", "JSON не имеет встроенных типов для них; требуется явное представление и симметричное восстановление."),
    ],
}


OTHER_DEEP = {
    "sql-01": [
        ("Что обеспечивают PRIMARY KEY и FOREIGN KEY?", "PRIMARY KEY однозначно идентифицирует строку; FOREIGN KEY запрещает ссылку на отсутствующую связанную строку и поддерживает ссылочную целостность."),
        ("Как моделировать отношение many-to-many между users и courses?", "Отдельной таблицей enrollments с внешними ключами user_id и course_id; их пара обычно образует составной PRIMARY KEY или UNIQUE."),
    ],
    "sql-02": [
        ("Как правильно проверить SQL NULL?", "Через <code>IS NULL</code> или <code>IS NOT NULL</code>. Сравнение <code>= NULL</code> даёт UNKNOWN, а не TRUE."),
        ("В каком порядке логически применяются WHERE, ORDER BY и LIMIT?", "Сначала WHERE отбирает строки, затем ORDER BY задаёт порядок, после этого LIMIT ограничивает результат."),
    ],
    "sql-03": [
        ("Чем LEFT JOIN отличается от INNER JOIN?", "INNER JOIN оставляет только совпавшие пары; LEFT JOIN сохраняет все строки слева и подставляет NULL справа при отсутствии совпадения."),
        ("Почему JOIN может размножить строки?", "Если одной строке слева соответствует несколько строк справа, результат содержит отдельную строку для каждого совпадения. Кардинальность нужно оценить до JOIN."),
    ],
    "sql-04": [
        ("Чем WHERE отличается от HAVING?", "WHERE фильтрует исходные строки до группировки; HAVING фильтрует уже сформированные группы и может использовать агрегаты."),
        ("Что считает <code>COUNT(column)</code> в отличие от <code>COUNT(*)</code>?", "<code>COUNT(column)</code> игнорирует NULL в этой колонке; <code>COUNT(*)</code> считает строки группы."),
    ],
    "sql-15": [
        ("Как безопасно выполнить массовый UPDATE?", "Сначала проверить тот же WHERE через SELECT, выполнить изменение в транзакции и использовать RETURNING для контроля фактически изменённых строк."),
        ("Для чего PostgreSQL-конструкция RETURNING?", "Возвращает строки, реально затронутые INSERT/UPDATE/DELETE, без отдельного запроса после изменения."),
    ],
    "sql-08": [
        ("Какие инварианты выражают NOT NULL, UNIQUE и CHECK?", "NOT NULL требует значение, UNIQUE запрещает дубли в ключе, CHECK проверяет логическое условие для строки."),
        ("Зачем нормализовать повторяющиеся данные?", "Чтобы одна сущность хранилась в одном месте, уменьшить дублирование и избежать аномалий вставки, обновления и удаления."),
    ],
    "testing-01": [
        ("Какие проверки нужны помимо happy path?", "Границы, неверные типы и значения, отсутствие данных, ошибки зависимостей, права доступа и повтор операции."),
        ("С чего начинать проектирование теста?", "С контракта и риска: какое наблюдаемое поведение важно и каким дефектом оно может быть нарушено."),
    ],
    "testing-02": [
        ("Что отличает unit-тест от integration-теста?", "Unit изолированно проверяет небольшую единицу логики; integration проверяет реальное взаимодействие компонентов, например приложения с БД."),
        ("Почему нельзя строить всю пирамиду только на E2E?", "E2E медленные, хрупкие и хуже локализуют причину. Ими покрывают критические пользовательские пути, а детали — более быстрыми тестами."),
    ],
    "testing-03": [
        ("Какие значения проверять для диапазона 1–100?", "Минимум 0, 1, 2, 99, 100, 101: точки непосредственно за границами, сами границы и соседние допустимые значения."),
        ("Что такое класс эквивалентности?", "Набор входов, для которых ожидается одинаковое поведение; из класса выбирают репрезентативное значение, а границы проверяют отдельно."),
    ],
    "testing-04": [
        ("Как pytest проверяет исключение?", "Через <code>with pytest.raises(ExpectedError): ...</code>; при необходимости проверяют сообщение через <code>match=</code>."),
        ("По каким соглашениям pytest обнаруживает тесты?", "Обычно файлы <code>test_*.py</code>/<code>*_test.py</code>, функции и методы <code>test_*</code>, классы <code>Test*</code> без собственного init."),
    ],
    "testing-05": [
        ("Как fixture выполняет teardown?", "Код до <code>yield</code> готовит ресурс, значение yield получает тест, код после yield освобождает ресурс даже при ошибке теста."),
        ("Что меняет scope fixture?", "Время жизни и частоту создания: function, class, module, package или session. Более широкий scope повышает риск разделяемого состояния."),
    ],
    "testing-06": [
        ("Как выглядит базовый parametrize?", "<pre><code>@pytest.mark.parametrize('value, expected', [(1, 2), (2, 4)])\ndef test_double(value, expected):\n    assert value * 2 == expected</code></pre>"),
        ("Зачем задавать ids параметрам?", "Чтобы отчёт называл сценарии по смыслу, а не индексами или длинным repr; это ускоряет диагностику падения."),
    ],
    "http-01": [
        ("Каков упрощённый путь HTTPS-запроса?", "DNS → TCP-соединение → TLS handshake и проверка сертификата → HTTP-запрос → reverse proxy → приложение → БД/зависимости → ответ."),
        ("Какой командой быстро проверить DNS и какой — HTTPS-ответ?", "Например <code>nslookup example.com</code> для DNS и <code>curl -v https://example.com</code> для соединения, TLS и HTTP."),
    ],
    "http-02": [
        ("Когда использовать path parameter, а когда query parameter?", "Path идентифицирует конкретный ресурс: <code>/users/42</code>. Query изменяет выборку/представление: <code>?status=active&amp;limit=20</code>."),
        ("Почему секрет нельзя помещать в URL query?", "URL попадает в историю, логи, аналитику и Referer. Секрет передают предусмотренным механизмом авторизации по HTTPS."),
    ],
    "http-03": [
        ("Какие HTTP-методы считаются идемпотентными по семантике?", "GET, HEAD, OPTIONS, PUT и DELETE. POST обычно не идемпотентен; PATCH зависит от конкретной операции."),
        ("PUT или PATCH для частичного изменения одного поля?", "Обычно PATCH. PUT семантически заменяет полное представление ресурса по известному URI."),
    ],
    "http-04": [
        ("Когда вернуть 201, а когда 204?", "201 — ресурс создан, желательно с Location; 204 — запрос успешен, но тело ответа отсутствует."),
        ("Чем 401 отличается от 403 и 409 от 422?", "401 — нет действительной аутентификации; 403 — личность известна, но доступ запрещён; 409 — конфликт состояния; 422 — семантически неверные входные данные."),
    ],
    "http-06": [
        ("Как назвать endpoint списка курсов и зачислений без RPC-глаголов?", "Например <code>GET /courses</code>, <code>POST /courses</code>, <code>POST /courses/{id}/enrollments</code>, а не <code>/getCourses</code> и <code>/enrollUser</code>."),
        ("Когда вложенность ресурсов становится вредной?", "Когда URL отражает длинную цепочку реализации. Обычно достаточно ближайшего владельца; глубоко вложенный ресурс лучше адресовать собственным ID."),
    ],
    "http-07": [
        ("Что должно быть в стабильной ошибке API?", "Машинно-читаемый code, понятное message, детали по полям при необходимости и correlation/request ID; HTTP-статус должен соответствовать классу ошибки."),
        ("Чем проверка формы отличается от бизнес-валидации?", "Форма проверяет типы, обязательность и формат; бизнес-правило проверяет допустимость операции в текущем состоянии предметной области."),
    ],
    "git-01": [
        ("Что хранят blob, tree и commit?", "Blob — содержимое файла; tree — имена и ссылки на blobs/trees; commit — ссылку на корневой tree, родителей и метаданные."),
        ("Что такое branch и HEAD?", "Branch — подвижный указатель на commit; HEAD указывает на текущую ветку либо непосредственно на commit в detached-состоянии."),
    ],
    "git-02": [
        ("Какими командами сравнить рабочее дерево и index?", "<code>git diff</code> показывает unstaged, <code>git diff --staged</code> — staged изменения относительно HEAD."),
        ("Каков путь изменения до истории Git?", "Файл меняется в working tree → <code>git add</code> помещает версию в index → <code>git commit</code> создаёт commit из index."),
    ],
    "git-19": [
        ("Почему добавление файла в .gitignore не скрывает уже tracked файл?", "Ignore применяется к untracked путям. Нужно перестать отслеживать файл отдельно; секрет при этом всё равно остаётся в старой истории."),
        ("Для чего полезен .gitattributes?", "Для правил обработки путей: line endings, linguist/diff/merge drivers, binary/text и export-ignore."),
    ],
    "git-03": [
        ("Какие команды проверить перед commit?", "Минимум <code>git status</code>, <code>git diff</code>, <code>git diff --staged</code> и релевантные тесты."),
        ("Что делает commit атомарным по смыслу?", "Одна логическая причина изменения, рабочее состояние и сообщение, объясняющее намерение, а не перечисляющее файлы."),
    ],
    "git-04": [
        ("Что делает <code>git switch -c feature/name</code>?", "Создаёт новую ветку на текущем commit и переключает working tree/HEAD на неё."),
        ("Почему ветка в Git дешева?", "Это небольшой указатель на commit, а не копия всего каталога проекта."),
    ],
    "git-09": [
        ("Чем fetch отличается от pull?", "fetch только получает объекты и обновляет remote-tracking refs; pull затем ещё интегрирует изменения через merge или rebase."),
        ("Что публикует <code>git push origin main</code>?", "Передаёт недостающие объекты и просит обновить ветку main на remote origin; при несовместимой истории push обычно отклоняется."),
    ],
    "git-05": [
        ("Когда merge будет fast-forward?", "Когда текущая ветка является предком присоединяемой: указатель можно просто передвинуть вперёд без merge commit."),
        ("Что нужно проверить после разрешения merge-конфликта?", "Итоговую семантику файла, отсутствие маркеров, diff и тесты; затем добавить исправленные файлы и завершить merge."),
    ],
    "git-07": [
        ("Что означают маркеры <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>, <code>=======</code>, <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code>?", "Границы двух конфликтующих вариантов. Их нельзя просто удалить: нужно собрать правильное итоговое содержимое."),
        ("Почему выбор ours/theirs не является универсальным решением?", "Он целиком берёт одну сторону и может потерять нужную часть другой; смысл объединения определяется требуемым поведением."),
    ],
    "linux-01": [
        ("Какие команды показывают текущий каталог и его содержимое?", "<code>pwd</code> печатает рабочий каталог; <code>ls -la</code> показывает в том числе скрытые записи и подробные атрибуты."),
        ("Чем абсолютный путь отличается от относительного?", "Абсолютный начинается от <code>/</code>; относительный разрешается от текущего рабочего каталога процесса."),
    ],
    "linux-02": [
        ("Что означает режим <code>chmod 640 file</code>?", "Owner: read+write; group: read; others: никаких прав."),
        ("Почему chmod 777 — плохое исправление?", "Он выдаёт запись и выполнение всем пользователям, маскирует проблему владельца/группы и нарушает принцип минимальных прав."),
    ],
    "linux-03": [
        ("Как следить за дописываемым логом и искать ERROR?", "Например <code>tail -F app.log | grep ERROR</code>; для быстрого поиска по файлам удобен <code>rg 'ERROR'</code>."),
        ("Как создать и распаковать gzip-архив каталога?", "Создать: <code>tar -czf backup.tar.gz dir/</code>; распаковать: <code>tar -xzf backup.tar.gz</code>."),
    ],
    "linux-04": [
        ("Чем отличаются <code>&gt;</code>, <code>&gt;&gt;</code> и <code>2&gt;</code>?", "<code>&gt;</code> перезаписывает stdout-файл, <code>&gt;&gt;</code> дописывает stdout, <code>2&gt;</code> перенаправляет stderr."),
        ("Что делает pipe?", "Передаёт stdout процесса слева в stdin процесса справа; stderr отдельно не передаётся без явного перенаправления."),
    ],
    "linux-06": [
        ("Как посмотреть exit code последней команды в POSIX shell?", "Через <code>echo $?</code>; 0 обычно означает успех, ненулевое значение — конкретный класс ошибки."),
        ("Почему переменную пути обычно пишут как <code>\"$path\"</code>?", "Кавычки предотвращают word splitting и glob expansion, поэтому путь с пробелами остаётся одним аргументом."),
    ],
    "linux-13": [
        ("Чем системный пакет отличается от Python-пакета?", "Системный менеджер устанавливает библиотеки и программы ОС; pip управляет Python-дистрибутивами, желательно внутри venv."),
        ("Почему опасна команда <code>curl URL | sudo sh</code>?", "Удалённый непроверенный код сразу выполняется с root-правами; источник, подпись/хеш и содержимое нужно проверить до запуска."),
    ],
    "django-01": [
        ("Каков основной маршрут Django request?", "ASGI/WSGI server → middleware → URL resolver → view → при необходимости ORM/template/serializer → response → обратный проход middleware."),
        ("Когда QuerySet обычно обращается к БД?", "При вычислении: итерации, list(), len() в ряде случаев, bool(), repr/срезе с шагом и других операциях, требующих результата."),
    ],
    "django-02": [
        ("Что задаёт <code>on_delete</code> у ForeignKey?", "Поведение зависимых строк при удалении объекта: CASCADE, PROTECT, RESTRICT, SET_NULL и другие варианты; выбор должен отражать предметную область."),
        ("Для чего нужен <code>related_name</code>?", "Задаёт понятное имя обратной связи, например <code>course.lessons.all()</code>, и предотвращает конфликт стандартных имён."),
    ],
    "docker-01": [
        ("Чем image отличается от container?", "Image — неизменяемый шаблон слоёв; container — запущенный или остановленный экземпляр с собственным writable layer и процессом."),
        ("Какими командами показать images и containers?", "<code>docker image ls</code> и <code>docker container ls -a</code>. Удаление container не удаляет исходный image."),
    ],
    "docker-02": [
        ("Чем CMD отличается от RUN в Dockerfile?", "RUN выполняется при сборке и создаёт слой; CMD задаёт команду по умолчанию при запуске container."),
        ("Почему COPY requirements перед COPY всего проекта ускоряет rebuild?", "Слой установки зависимостей остаётся в cache, пока файл зависимостей не изменился; изменения приложения не заставляют переустанавливать пакеты."),
    ],
}


def stable_number(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big") >> 1


def clean(value: str) -> str:
    return html.escape(value, quote=False).replace("\n", "<br>")


def syntax_cards(topic: dict, exact_cards: list[tuple[str, str]]):
    """Turn every explicitly authored inline command/operator into direct recall."""
    seen = set()
    skip = {"[1] True", "[1]", "stop-start", "middle", "None", "/", "*", "try", "return", "for"}
    for question, answer in exact_cards:
        for token in re.findall(r"<code>(?!<)(.*?)</code>", question + answer, flags=re.DOTALL):
            token = token.strip()
            if not token or token in skip or "\n" in token or len(token) > 80 or token in seen:
                continue
            seen.add(token)
            yield (
                f'Что означает или что делает <code>{token}</code>?',
                f'{answer}<br><br><span class="source">Контекст: {clean(topic["title"])}</span>',
            )


def concrete_case_cards(topic: dict, theory: str):
    task = topic["tasks"][-1]
    case = clean(task.get("case") or task["statement"])
    deliverable = clean(task.get("deliverable") or "Запускаемый минимальный пример с проверкой результата.")
    artifact = clean(task.get("artifact") or "Минимальный воспроизводимый пример")
    return [
        (
            f'Напиши решение без подсказки: {case}',
            f'Решение должно непосредственно демонстрировать правило: {theory}<br><br>Критерий результата: {deliverable}',
        ),
        (
            f'Какой проверяемый артефакт предъявить для задачи: {case}',
            f'<code>{artifact}</code><br><br>{deliverable}',
        ),
    ]


def applied_cards(track: dict, topic: dict, theory: str, pitfall: str, case: str):
    task = topic["tasks"][-1]
    deliverable = clean(task.get("deliverable") or "Короткое решение и проверяемый результат.")
    artifact = clean(task.get("artifact") or "Минимальный воспроизводимый пример.")
    exact = PYTHON_DEEP.get(topic["id"], []) + OTHER_DEEP.get(topic["id"], [])
    exact_answer = "<br><br>".join(f'<b>{q}</b><br>{a}' for q, a in exact)
    medium = {
        "python": "запускаемый фрагмент Python",
        "sql": "SQL-запрос или DDL",
        "testing": "pytest-тест",
        "http": "HTTP-запрос и ожидаемый ответ",
        "git": "последовательность Git-команд и проверку diff/status",
        "linux": "безопасную shell-команду и проверку exit code",
        "django": "минимальный Django-сценарий и проверку БД/response",
        "docker": "Docker-команду или фрагмент Dockerfile и проверку результата",
    }.get(track["id"], "минимальный воспроизводимый пример")
    title = clean(topic["title"])
    return [
        (
            f'Практика без подсказки: создай {medium}, который демонстрирует тему «{title}».',
            f'Минимальный критерий: пример действительно показывает правило «{theory}». Результат нужно запустить или проверить, а не только написать.'
        ),
        (
            f'Разбери кейс по теме «{title}»: {case}',
            f'Ответ должен содержать предположение, конкретное действие, наблюдаемый результат и объяснение через правило: {theory}'
        ),
        (
            f'Воспроизведи по памяти точный синтаксис, команду или ключевое различие для темы «{title}».',
            exact_answer or f'Опорное правило: {theory}'
        ),
        (
            f'Какой граничный или отрицательный сценарий обязательно проверить для темы «{title}»?',
            f'Проверь сценарий, в котором проявляется ошибка «{pitfall}», а также минимум один пустой, отсутствующий, повторный или крайний ввод — тот, который применим к механизму.'
        ),
        (
            f'Исправление дефекта: в реализации обнаружено «{pitfall}». Что должно измениться?',
            f'Исправление обязано восстановить правило «{theory}». После исправления сначала воспроизведи старый дефект, затем добавь regression-проверку.'
        ),
        (
            f'Как протестировать практическое применение темы «{title}»?',
            f'Нужны минимум три проверки: нормальный случай, граничный случай и сценарий ошибки «{pitfall}». Каждая проверка должна утверждать наблюдаемый результат.'
        ),
        (
            f'Какой проверяемый результат нужно сохранить после практики по теме «{title}»?',
            f'{deliverable}<br>Ожидаемый артефакт: <code>{artifact}</code>'
        ),
        (
            f'Production-разбор по теме «{title}»: как действовать, если механизм ведёт себя не так, как ожидалось?',
            f'1) Зафиксировать симптомы и входные данные. 2) Проверить предпосылки правила «{theory}». 3) Получить минимальное воспроизведение. 4) Исправить причину, связанную с «{pitfall}». 5) Подтвердить исправление тестом или измерением.'
        ),
    ]


def topic_cards(track: dict, topic: dict, day: dict, completed: bool):
    theory = clean(topic["theory"])
    pitfall = clean(topic["pitfall"])
    status = "пройдено" if completed else "по плану"
    status_tag = "completed" if completed else "planned"
    context = f'{day["date"].strftime("%d.%m.%Y")} · {track["title"]} · {topic["title"]} · {status}'
    source = f'Трекер Eidos · {topic["id"]} · план до 10.10.2026'
    qa = [
        (f'Что означает и как работает «{clean(topic["title"])}»?', theory),
        (f'Почему неверен или опасен подход: «{pitfall}»?', f'Правильное правило: {theory}'),
    ]
    exact_cards = PYTHON_DEEP.get(topic["id"], []) + OTHER_DEEP.get(topic["id"], [])
    qa.extend(exact_cards)
    qa.extend(syntax_cards(topic, exact_cards))
    qa.extend(EXTRA_CONCRETE.get(topic["id"], []))
    qa.extend(concrete_case_cards(topic, theory))
    for index, (question, answer) in enumerate(qa, 1):
        yield {
            "id": f'{topic["id"]}-{index:02d}',
            "question": question,
            "answer": answer,
            "context": context,
            "source": source,
            "tags": ["eidos", track["id"], topic["id"], status_tag, f'day-{day["number"]:02d}'],
            "deck": 'Eidos — Python Backend до 10 октября',
        }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    solved = set(state.get("completed", []))
    prompt_ready = set(state.get("prompt_ready", []))
    topics = []
    seen = set()
    for day in build_daily_plan():
        if day["date"] > DEADLINE:
            continue
        for track, topic in day["topics"]:
            if topic["id"] in seen:
                continue
            seen.add(topic["id"])
            completed = topic["id"] in prompt_ready and all(task["id"] in solved for task in topic["tasks"])
            topics.append((track, topic, day, completed))

    cards = [card for args in topics for card in topic_cards(*args)]
    decks = {}
    for card in cards:
        if card["deck"] not in decks:
            decks[card["deck"]] = genanki.Deck(stable_number(card["deck"]), card["deck"])
        note = genanki.Note(
            model=MODEL,
            fields=[card["id"], card["question"], card["answer"], card["context"], card["source"]],
            tags=card["tags"],
            guid=genanki.guid_for(card["id"]),
        )
        decks[card["deck"]].add_note(note)

    apkg = OUTPUT / "eidos_python_backend_through_2026-10-10.apkg"
    genanki.Package(list(decks.values())).write_to_file(str(apkg))

    tsv = OUTPUT / "eidos_python_backend_through_2026-10-10.tsv"
    with tsv.open("w", encoding="utf-8", newline="") as handle:
        handle.write("#separator:Tab\n#html:true\n#columns:ID\tQuestion\tAnswer\tContext\tSource\tTags\tDeck\n")
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        for card in cards:
            writer.writerow([card["id"], card["question"], card["answer"], card["context"], card["source"], " ".join(card["tags"]), card["deck"]])

    counts = {}
    for card in cards:
        topic_id = next(tag for tag in card["tags"] if "-" in tag and not tag.startswith("day-"))
        counts[topic_id] = counts.get(topic_id, 0) + 1
    manifest = OUTPUT / "README.md"
    done = sum(completed for _track, _topic, _day, completed in topics)
    lines = [
        "# Eidos Anki deck",
        "",
        f"- Тем: {len(topics)}",
        f"- Карточек: {len(cards)}",
        f"- Уже завершено по трекеру: {done}",
        f"- Ещё по плану: {len(topics) - done}",
        "- Последняя дата: 10.10.2026",
        "",
        "## Состав",
        "",
    ]
    for track, topic, day, completed in topics:
        lines.append(f'- {day["date"].strftime("%d.%m")} · {topic["id"]} · {topic["title"]} · {counts[topic["id"]]} карточек · {"пройдено" if completed else "по плану"}')
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"topics": len(topics), "cards": len(cards), "completed_topics": done, "apkg": str(apkg), "tsv": str(tsv)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
