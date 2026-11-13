"""Two-page resumes focused on independent lead-management development."""
from copy import deepcopy
import json

from build_resume_balanced import BalancedResume, CONTENT

JEWELRY = deepcopy(CONTENT)
for content in JEWELRY.values():
    content['results_first'] = True
    content['include_project'] = False
JEWELRY['RU'].update({
 'job': 'Python-разработчик | Ювелирная компания',
 'summary': 'Python-разработчик с 3 годами опыта. Самостоятельно разрабатывал и поддерживал внутреннюю систему работы с лидами для компании, занимающейся разработкой ювелирных изделий. Основной стек - Django, Django REST Framework и PostgreSQL. Работал с API, интеграциями, фоновыми задачами и выпуском изменений.',
 'scope': 'Внутренняя система учёта лидов и клиентских заявок. Вёл разработку самостоятельно: уточнял потребности бизнеса, дорабатывал backend, проверял изменения и поддерживал приложение после выпуска.',
 'responsibilities': [
 'Разрабатывал REST API на Django/DRF для создания и обновления лидов, хранения контактных данных и изменения статусов заявок. Добавлял валидацию, поиск, фильтрацию и пагинацию.',
 'Работал с моделями Django ORM и PostgreSQL: менял структуру данных через миграции, писал SQL-запросы и проверял выборки. Использовал Redis для кэширования.',
 'Подключал внешние API для обмена данными по заявкам. Поддерживал отдельные endpoints на FastAPI и фоновые задачи Celery с обработкой ошибок, тайм-аутами и повторами.',
 'Самостоятельно проверял и выпускал изменения: писал тесты, использовал Docker и GitHub Actions, применял миграции, разбирал ошибки по логам и обновлял документацию.',
 ],
 'results_title': 'Основные результаты',
 'required_first_page': ['74 до 11', '920 до 240 мс', '87%', '40 до 10 минут'],
 'results': [
 'Сократил число SQL-запросов к каталогу <b>с 74 до 11</b>, p95 времени ответа - <b>с 920 до 240 мс</b> при одинаковой нагрузке и данных. Устранил N+1 и подобрал индексы с EXPLAIN ANALYZE.',
 'Довёл покрытие прикладного backend-кода до <b>87% строк</b> с pytest. Добавил тесты прав доступа, повторных запросов и ошибок внешних API.',
 'Сократил время типового релиза <b>с 40 до 10 минут</b>: автоматизировал сборку и выпуск через Docker и GitHub Actions, включая тесты, миграции и проверки доступности.',
 ],
 'work_groups': [
 ('Лиды, заявки и данные', [
 'Разрабатывал API для карточки лида: контактные данные, сведения о запросе клиента и статус обработки. Проверял входные данные и права доступа при чтении и изменении записей.',
 'Дорабатывал поиск и фильтры для списка заявок. Менял модели и связи через миграции, проверял запросы Django ORM и устранял лишние обращения к PostgreSQL.',
 'Использовал Redis для кэширования часто запрашиваемых данных: задавал срок хранения и обновлял кэш при изменениях. Описывал форматы запросов и ответов API.',
 ]),
 ('Интеграции и фоновые задачи', [
 'Поддерживал получение и передачу данных о заявках через внешние API. Проверял HTTP-статусы и формат ответа, обрабатывал тайм-ауты и сохранял ошибки в логах.',
 'Выносил длительную обработку в Celery с RabbitMQ. Настраивал ограниченные повторы при временных сбоях и сохранял статус обработки для проверки через API.',
 'При обработке webhook проверял идентификатор события, чтобы повторная доставка не создавала повторную запись. Использовал транзакции и ограничения уникальности.',
 ]),
 ('Самостоятельная разработка и поддержка', [
 'Уточнял, что нужно изменить в работе с заявками, разбивал доработку на небольшие задачи и проверял сценарий перед выпуском. Вёл код в Git и документировал изменения.',
 'Писал тесты API и бизнес-логики с pytest, подменял внешние ответы в тестах. Проверял сборку и тесты в CI, после развёртывания смотрел логи и исправлял обнаруженные ошибки.',
 ]),
 ],
})
JEWELRY['EN'].update({
 'job': 'Python Backend Developer | Jewelry Company',
 'summary': 'Python developer with 3 years of experience. Independently developed and maintained an internal lead-management system for a jewelry design company. Main stack: Django, Django REST Framework and PostgreSQL. Worked on APIs, integrations, background tasks and releases.',
 'scope': 'An internal system for tracking leads and customer inquiries. Handled development independently: clarified business needs, updated the backend, tested changes and maintained the application after releases.',
 'responsibilities': [
 'Developed Django/DRF REST APIs to create and update leads, store contact details and change inquiry statuses. Added validation, search, filtering and pagination.',
 'Worked with Django ORM models and PostgreSQL: updated schemas through migrations, wrote SQL queries and reviewed data retrieval. Used Redis for caching.',
 'Integrated external APIs to exchange inquiry data. Maintained individual FastAPI endpoints and Celery background tasks with error handling, timeouts and retries.',
 'Independently tested and released changes: wrote tests, used Docker and GitHub Actions, applied migrations, investigated errors through logs and updated documentation.',
 ],
 'results_title': 'Selected results',
 'required_first_page': ['74 to 11', '920 to 240 ms', '87%', '40 to 10 minutes'],
 'results': [
 'Reduced SQL queries per catalog request <b>from 74 to 11</b> and p95 latency <b>from 920 to 240 ms</b> under the same load and dataset. Removed N+1 queries and tuned indexes using EXPLAIN ANALYZE.',
 'Reached <b>87% line coverage</b> of application backend code with pytest. Added tests for access permissions, duplicate requests and external API failures.',
 'Cut typical release time <b>from 40 to 10 minutes</b> by automating builds and releases with Docker and GitHub Actions, including tests, migrations and health checks.',
 ],
 'work_groups': [
 ('Leads, inquiries and data', [
 'Developed APIs for lead records containing contact details, customer inquiry information and processing status. Validated input and checked permissions when reading or updating records.',
 'Updated search and filters for inquiry lists. Changed models and relationships through migrations, reviewed Django ORM queries and removed unnecessary PostgreSQL calls.',
 'Used Redis to cache frequently requested data, configured expiration times and refreshed cached data after changes. Documented API request and response formats.',
 ]),
 ('Integrations and background tasks', [
 'Maintained incoming and outgoing inquiry data exchange through external APIs. Checked HTTP status codes and response formats, handled timeouts and logged errors.',
 'Moved long-running processing to Celery with RabbitMQ. Configured bounded retries for temporary failures and stored processing status for checking through the API.',
 'Checked webhook event identifiers to prevent repeated delivery from creating duplicate records. Used transactions and uniqueness constraints.',
 ]),
 ('Independent development and support', [
 'Clarified required changes to inquiry workflows, broke updates into small tasks and checked the relevant scenario before release. Managed code in Git and documented changes.',
 'Wrote API and business-logic tests with pytest and mocked external responses. Checked builds and tests in CI, reviewed logs after deployment and fixed reported errors.',
 ]),
 ],
})

if __name__ == '__main__':
    results = []
    for lang in ('RU', 'EN'):
        result = BalancedResume(lang, JEWELRY, 'Jewelry').build()
        results.append(result)
    print(json.dumps(results, ensure_ascii=False, indent=2))
