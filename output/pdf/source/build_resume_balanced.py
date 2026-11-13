"""Two-page editorial resumes with task-focused descriptions."""
from pathlib import Path
from copy import deepcopy
import json
import re
from html import unescape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
from build_resume import Resume, DATA, link, W, H, MUTED

OUT = Path(__file__).resolve().parents[1]
CONTENT = deepcopy(DATA)
CONTENT['RU'].update({
 'role': 'Python Backend Developer / Python-разработчик',
 'summary': 'Python-разработчик с 3 годами опыта в B2B SaaS. Разрабатываю и поддерживаю REST API, работаю с PostgreSQL, интеграциями и фоновыми задачами. Основной стек - Django и Django REST Framework. Участвую в тестировании и выпуске изменений.',
 'skills': [
 '<b>Backend:</b> Python, Django, Django REST Framework, FastAPI, REST API, HTTP, JWT.',
 '<b>Данные:</b> PostgreSQL, SQL, Django ORM, Redis.',
 '<b>Фоновые задачи:</b> Celery, RabbitMQ.',
 '<b>Тестирование:</b> pytest, unit- и интеграционные тесты, моки внешних API.',
 '<b>Инструменты:</b> Git, Linux, Docker, Docker Compose, GitHub Actions.',
 '<b>Дополнительно:</b> JavaScript, React для работы с интерфейсами.',
 ],
 'scope': 'Платформа с личными кабинетами, управлением доступом и внешними интеграциями. Занимался доработкой backend-функций, исправлением ошибок и поддержкой существующих сервисов.',
 'responsibility_title': 'Основные задачи',
 'responsibilities': [
 'Разрабатывал и дорабатывал REST API на Django/DRF: обработка запросов, валидация данных, права доступа, фильтрация и пагинация. Поддерживал отдельные endpoints на FastAPI.',
 'Работал с моделями и запросами Django ORM, писал SQL-запросы к PostgreSQL, создавал миграции. Использовал Redis для кэширования данных.',
 'Подключал внешние API и поддерживал фоновые задачи на Celery. Обрабатывал ошибки запросов, настраивал тайм-ауты и повторные попытки.',
 'Писал тесты, участвовал в code review и обсуждении задач. Проверял изменения перед релизом, разбирал ошибки по логам и обновлял документацию.',
 ],
 'results_title': 'Примеры доработок',
 'results': [
 'Оптимизировал запросы к каталогу: убирал лишние обращения к базе, использовал загрузку связанных объектов и индексы для часто используемых выборок.',
 'Добавлял проверки прав доступа и обработки ошибок внешних API. После исправления ошибок дополнял тесты, чтобы проверять эти сценарии при следующих изменениях.',
 'Участвовал в настройке сборки и проверок через Docker и GitHub Actions. Поддерживал команды запуска приложения и применение миграций.',
 ],
 'details_title': 'Опыт работы: подробнее о задачах',
 'work_groups': [
 ('API и работа с данными', [
 'Дорабатывал endpoints для личных кабинетов и управления доступом. Проверял входные данные, возвращал понятные ошибки и учитывал права пользователя при получении и изменении данных.',
 'Изменял модели и схему базы через миграции. Проверял выборки связанных объектов, устранял лишние запросы и разбирался с причинами медленной работы API.',
 'Поддерживал кэширование в Redis: задавал срок хранения и обновлял кэш при изменении исходных данных. Документировал изменения форматов запросов и ответов.',
 ]),
 ('Интеграции и фоновые задачи', [
 'Поддерживал запросы к внешним сервисам: проверял HTTP-статусы и формат ответа, обрабатывал тайм-ауты и сохранял информацию об ошибках в логах.',
 'Выносил длительную обработку в Celery, настраивал ограниченные повторы при временных сбоях. Сохранял статус обработки, чтобы его можно было получить через API.',
 'При обработке webhook проверял идентификатор события и учитывал повторную доставку. Использовал транзакции и ограничения уникальности для связанных изменений в базе.',
 ]),
 ('Тестирование и поддержка', [
 'Писал тесты бизнес-логики и API с pytest. Проверял успешные запросы, ошибки в данных и доступ без нужных прав; подменял ответы внешних сервисов в тестах.',
 'Проверял изменения локально и в CI. После релиза смотрел логи и доступность API, воспроизводил найденные ошибки и добавлял проверки после исправления.',
 ]),
 ],
})
CONTENT['EN'].update({
 'summary': 'Python developer with 3 years of experience in B2B SaaS. Develop and maintain REST APIs, work with PostgreSQL, service integrations and background tasks. Main stack: Django and Django REST Framework. Contribute to testing and releases.',
 'skills': [
 '<b>Backend:</b> Python, Django, Django REST Framework, FastAPI, REST API, HTTP, JWT.',
 '<b>Data:</b> PostgreSQL, SQL, Django ORM, Redis.',
 '<b>Background tasks:</b> Celery, RabbitMQ.',
 '<b>Testing:</b> pytest, unit and integration tests, mocking external APIs.',
 '<b>Tools:</b> Git, Linux, Docker, Docker Compose, GitHub Actions.',
 '<b>Additional:</b> JavaScript and React for interface development.',
 ],
 'scope': 'A platform with user accounts, access management and external integrations. Worked on backend feature updates, bug fixes and maintenance of existing services.',
 'responsibility_title': 'Main responsibilities',
 'responsibilities': [
 'Developed and updated REST APIs with Django/DRF: request handling, data validation, access permissions, filtering and pagination. Maintained individual FastAPI endpoints.',
 'Worked with Django ORM models and queries, wrote SQL queries for PostgreSQL and created migrations. Used Redis for data caching.',
 'Integrated external APIs and maintained Celery background tasks. Handled request errors, configured timeouts and retries.',
 'Wrote tests, took part in code reviews and task discussions. Checked changes before releases, investigated errors through logs and updated documentation.',
 ],
 'results_title': 'Selected improvements',
 'results': [
 'Optimized catalog queries by removing unnecessary database calls, loading related objects efficiently and using indexes for common queries.',
 'Added checks for access permissions and external API failures. Extended tests after bug fixes to cover those scenarios in future changes.',
 'Contributed to build and check configuration with Docker and GitHub Actions. Maintained application startup commands and migration steps.',
 ],
 'details_title': 'Experience: task details',
 'work_groups': [
 ('APIs and data', [
 'Updated endpoints for user accounts and access management. Validated input, returned clear error responses and checked user permissions when reading or changing data.',
 'Updated models and database schemas through migrations. Reviewed related-object queries, removed unnecessary database calls and investigated slow API responses.',
 'Maintained Redis caching with expiration times and cache updates when source data changed. Documented changes to request and response formats.',
 ]),
 ('Integrations and background tasks', [
 'Maintained requests to external services: checked HTTP status codes and response formats, handled timeouts and recorded errors in logs.',
 'Moved long-running processing to Celery and configured bounded retries for temporary failures. Stored processing status and exposed it through an API endpoint.',
 'Checked event identifiers when processing webhooks and accounted for repeated delivery. Used transactions and uniqueness constraints for related database changes.',
 ]),
 ('Testing and support', [
 'Wrote business-logic and API tests with pytest. Covered successful requests, invalid input and insufficient permissions; mocked external service responses in tests.',
 'Checked changes locally and in CI. Reviewed logs and API availability after releases, reproduced reported bugs and added regression checks after fixes.',
 ]),
 ],
})

class BalancedResume(Resume):
 def __init__(self, lang, content=None, suffix='Balanced'):
    self.lang, self.d = lang, (CONTENT if content is None else content)[lang]
    self.path = OUT / f'Alexey_Python_Backend_{lang}_{suffix}.pdf'
    self.c = canvas.Canvas(str(self.path), pagesize=A4, pageCompression=1)
    self.c.setTitle(self.d['name'] + ' | Python Backend Developer')
    self.c.setAuthor(self.d['name'])
    self.c.setSubject('Python backend resume')
    self.y, self.bottoms = 32, []
 def header(self):
    photo = self.d.get('photo')
    header_width = W - 86 - (102 if photo else 0)
    self.p(self.d['name'], 'name', 4, width=header_width)
    self.p(self.d['role'], 'role', 6, width=header_width)
    self.p(self.d['location'], 'small', 3, width=header_width)
    if self.d.get('contacts'):
        for contact in self.d['contacts']:
            self.p(contact, 'small', 3, width=header_width)
        self.y += 9
    else:
        self.p(link('https://github.com/Middlewarer', 'github.com/Middlewarer'), 'small', 12, width=header_width)
    if photo:
        self.c.drawImage(photo, W-43-80, H-32-100, width=80, height=100,
                         preserveAspectRatio=True, anchor='c', mask='auto')
        self.y = max(self.y, 144)
 def footer(self, n):
    assert self.y < 786, (self.lang, n, self.y)
    self.bottoms.append(round(self.y, 1))
    self.c.setLineWidth(.5)
    self.c.setStrokeColor(HexColor('#DCE2E7'))
    self.c.line(43, 36, W-43, 36)
    self.c.setFillColor(HexColor(MUTED))
    self.c.setFont('Calibri', 8)
    self.c.drawString(43, 23, self.d['name'] + ' | Python Backend Developer')
    self.c.drawRightString(W-43, 23, f'{n} / 2')
 def build(self):
    d = self.d
    self.header()
    if d.get('summary_title'):
        self.section(d['summary_title'])
    self.p(d['summary'])
    self.section(d['skills_title'])
    for line in d['skills']: self.p(line, 'skills')
    self.section(d['exp_title'])
    self.p(d['job'], 'job', 3)
    self.p(d['dates'], 'small', 6)
    self.p(d['scope'])
    blocks = [('responsibility_title', 'responsibilities'), ('results_title', 'results')]
    if d.get('results_first', False):
        blocks.reverse()
    for title_key, items_key in blocks:
        if d.get('tasks_on_second_page') and items_key == 'responsibilities':
            continue
        self.sub(d[title_key])
        for line in d[items_key]: self.bullet(line)
    self.footer(1)
    self.c.showPage()
    self.y = 32
    self.p(d['name'] + ' | Python Backend Developer', 'small', 6)
    if d.get('tasks_on_second_page'):
        self.section(d['responsibility_title'])
        for line in d['responsibilities']: self.bullet(line)
    if d.get('include_details', True):
        self.section(d['details_title'])
        self.p(d['job'], 'small', 2)
        self.p(d['dates'], 'small', 2)
        for title, items in d['work_groups']:
            self.sub(title)
            for line in items: self.bullet(line)
    self.section(d['education_title'])
    self.p(d['education'], 'small')
    if d.get('languages'):
        self.section(d['languages_title'])
        for language in d['languages']:
            self.p(language, 'small')
    if d.get('include_project', True):
        self.section(d['project_title'])
        self.p(d['project_brief'], 'small', 4)
        self.p(link('https://eidosacademy.ru', 'eidosacademy.ru') + ' | ' + link('https://github.com/Middlewarer/EidosAcademy', 'github.com/Middlewarer/EidosAcademy'), 'small')
    self.footer(2)
    self.c.save()
    reader = PdfReader(self.path)
    assert len(reader.pages) == 2
    text = '\n\n'.join(page.extract_text() for page in reader.pages)
    normalized_text = ' '.join(text.split())
    assert d['dates'] in normalized_text and d['job'] in normalized_text
    for required in d.get('required_text', []):
        assert required in normalized_text, (self.lang, required)
    for forbidden in d.get('forbidden_text', []):
        assert forbidden not in normalized_text, (self.lang, forbidden)
    if not d.get('include_details', True):
        assert normalized_text.count(d['job']) == 1
        assert normalized_text.count(d['dates']) == 1
        assert d['details_title'] not in normalized_text
    if d.get('photo'):
        xobjects = reader.pages[0]['/Resources']['/XObject'].get_object()
        assert any(obj.get_object().get('/Subtype') == '/Image' for obj in xobjects.values())
    assert all(t not in text for t in ['Макет:', 'Sample:', 'Место для фото'])
    first_page = ' '.join(reader.pages[0].extract_text().split())
    for required in d.get('required_first_page', []):
        assert required in first_page, (self.lang, required)
    if d.get('results_first', False):
        assert normalized_text.index(d['results_title']) < normalized_text.index(d['responsibility_title'])
    if not d.get('include_project', True):
        assert d['project_title'] not in text
        assert 'eidosacademy' not in text.lower()
        for page in reader.pages:
            for annotation in page.get('/Annots', []):
                uri = annotation.get_object().get('/A', {}).get('/URI', '')
                assert 'eidosacademy' not in str(uri).lower()
    self.path.with_suffix('.txt').write_text(text, encoding='utf-8')
    return {'path': str(self.path), 'pages': len(reader.pages), 'body_bottoms': self.bottoms}

if __name__ == '__main__':
    print(json.dumps([BalancedResume(lang).build() for lang in ('RU', 'EN')], ensure_ascii=False, indent=2))
