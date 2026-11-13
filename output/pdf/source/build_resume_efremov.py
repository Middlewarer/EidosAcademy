"""User-requested employer, dates, portrait and languages for both resumes."""
from copy import deepcopy
import json
from build_resume_balanced import BalancedResume
from build_resume_jewelry import JEWELRY
from build_resume import link

EFREMOV = deepcopy(JEWELRY)
for content in EFREMOV.values():
    content['photo'] = 'C:/Users/onmyf/Downloads/Мое фото.png'
    content['forbidden_text'] = ['2023', '3 годами', '3 года', '3 years', 'B2B SaaS', '##', '**', '```']
    content['include_details'] = False
    content['tasks_on_second_page'] = True
    content['contacts'] = [
        link('mailto:leha.grabchuk@bk.ru', 'leha.grabchuk@bk.ru') + ' | ' + link('tel:+79610079773', '+7 961 007 97 73'),
        'Telegram: ' + link('https://t.me/Middlewarer', '@Middlewarer') + ' | ' + link('https://github.com/Middlewarer', 'github.com/Middlewarer'),
    ]

EFREMOV['RU'].update({
    'job': 'Python-разработчик | EFREMOV, ювелирная компания, Ярославль',
    'dates': 'Август 2024 - апрель 2026',
    'summary_title': 'О себе',
    'summary': 'Python Backend Developer, около 2 лет коммерческой разработки на <b>Django/DRF и PostgreSQL</b>. Домен - автоматизация работы с лидами и клиентскими заявками в ювелирном бизнесе. Сократил число SQL-запросов к каталогу <b>с 74 до 11</b> и p95 ответа <b>с 920 до 240 мс</b>; довёл покрытие backend-кода тестами до <b>87% строк</b>. Ищу удалённую работу в Python backend-разработке.',
    'scope': 'Самостоятельная разработка и поддержка backend внутренней системы учёта лидов и клиентских заявок.',
    'responsibility_title': 'Основные задачи и зона ответственности',
    'responsibilities': [
        '<b>API и бизнес-логика.</b> Разрабатывал REST API на Django/DRF для карточек лидов, контактных данных и статусов заявок. Добавлял поиск, фильтрацию, пагинацию, валидацию и проверки прав доступа; поддерживал отдельные endpoints на FastAPI.',
        '<b>База данных и кэш.</b> Работал с PostgreSQL, SQL и Django ORM: модели, связи, миграции и выборки. Настраивал кэширование в Redis со сроком хранения и обновлением при изменении исходных данных.',
        '<b>Интеграции.</b> Подключал внешние API для обмена данными по заявкам. Проверял HTTP-статусы и форматы ответов, обрабатывал тайм-ауты и сохранял ошибки в логах.',
        '<b>Фоновые задачи.</b> Выносил длительную обработку в Celery/RabbitMQ, настраивал ограниченные повторы и получение статуса через API. Защищал обработку webhook от повторного выполнения с помощью идентификаторов событий, транзакций и ограничений уникальности.',
        '<b>Тестирование.</b> Писал unit- и интеграционные тесты на pytest с моками внешних сервисов. Проверял бизнес-логику, ошибочные данные и права доступа; добавлял регрессионные сценарии после исправлений.',
        '<b>Выпуск и поддержка.</b> Уточнял требования, разбивал доработки на задачи, вёл код в Git. Проверял изменения локально и в CI, использовал Docker и GitHub Actions, применял миграции и проверял доступность после выпуска. Документировал API и разбирал ошибки по логам.',
    ],
    'education': '<b>Костромской государственный университет</b><br/>Информационные системы и технологии<br/>Бакалавриат, обучение продолжается (3-й курс).',
    'languages_title': 'Языки',
    'languages': ['<b>Русский:</b> родной.', '<b>Английский:</b> B2.', '<b>Румынский:</b> A2.'],
    'required_text': ['EFREMOV', 'Ярославль', 'Август 2024 - апрель 2026', 'Русский: родной.', 'Английский: B2.', 'Румынский: A2.'],
})
EFREMOV['EN'].update({
    'job': 'Python Backend Developer | EFREMOV, Jewelry Company, Yaroslavl',
    'dates': 'August 2024 - April 2026',
    'summary_title': 'Profile',
    'summary': 'Python Backend Developer with nearly 2 years of commercial development using <b>Django/DRF and PostgreSQL</b>. Domain: lead and customer inquiry automation in the jewelry industry. Reduced SQL queries per catalog request <b>from 74 to 11</b> and p95 latency <b>from 920 to 240 ms</b>; reached <b>87% line coverage</b> of backend code. Seeking a remote Python backend development role.',
    'scope': 'Independent development and maintenance of the backend for an internal lead and customer inquiry management system.',
    'responsibility_title': 'Responsibilities and technical scope',
    'responsibilities': [
        '<b>APIs and business logic.</b> Developed Django/DRF REST APIs for lead records, contact details and inquiry statuses. Added search, filtering, pagination, validation and access checks; maintained individual FastAPI endpoints.',
        '<b>Database and caching.</b> Worked with PostgreSQL, SQL and Django ORM on models, relationships, migrations and queries. Configured Redis caching with expiration times and updates when source data changed.',
        '<b>Integrations.</b> Connected external APIs to exchange inquiry data. Validated HTTP status codes and response formats, handled timeouts and logged errors.',
        '<b>Background processing.</b> Moved long-running work to Celery/RabbitMQ with bounded retries and task-status endpoints. Prevented duplicate webhook processing using event identifiers, transactions and uniqueness constraints.',
        '<b>Testing.</b> Wrote unit and integration tests with pytest and mocked external services. Tested business logic, invalid input and permissions; added regression scenarios after bug fixes.',
        '<b>Releases and support.</b> Clarified requirements, broke changes into tasks and managed code in Git. Checked changes locally and in CI, used Docker and GitHub Actions, applied migrations and verified availability after releases. Documented APIs and investigated errors through logs.',
    ],
    'education': '<b>Kostroma State University</b><br/>Information Systems and Technologies<br/>Bachelor\'s degree in progress (third year).',
    'languages_title': 'Languages',
    'languages': ['<b>Russian:</b> native.', '<b>English:</b> B2.', '<b>Romanian:</b> A2.'],
    'required_text': ['EFREMOV', 'Yaroslavl', 'August 2024 - April 2026', 'Russian: native.', 'English: B2.', 'Romanian: A2.'],
})

for content in EFREMOV.values():
    content['required_text'] += ['leha.grabchuk@bk.ru', '+7 961 007 97 73', 'Telegram: @Middlewarer']

if __name__ == '__main__':
    print(json.dumps([BalancedResume(lang, EFREMOV, 'Efremov').build()
                      for lang in ('RU', 'EN')], ensure_ascii=False, indent=2))
