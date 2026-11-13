"""Editorial versions of the supplied resumes; preserve the supplied career facts."""
from pathlib import Path
import json
import re
from html import unescape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from pypdf import PdfReader

from build_resume import DATA, link

OUT = Path(__file__).resolve().parents[1]
BLUE = colors.HexColor('#245478')
INK = colors.HexColor('#202B36')
MUTED = colors.HexColor('#576474')
STYLES = {
    'name': ParagraphStyle('name_hh', fontName='Calibri-Bold', fontSize=25, leading=28, textColor=INK, spaceAfter=2),
    'role': ParagraphStyle('role_hh', fontName='Calibri-Bold', fontSize=15, leading=19, textColor=BLUE, spaceAfter=5),
    'body': ParagraphStyle('body_hh', fontName='Calibri', fontSize=10.5, leading=13.5, textColor=INK, spaceAfter=4),
    'small': ParagraphStyle('small_hh', fontName='Calibri', fontSize=9.8, leading=12.5, textColor=MUTED, spaceAfter=3),
    'section': ParagraphStyle('section_hh', fontName='Calibri-Bold', fontSize=12, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True),
    'job': ParagraphStyle('job_hh', fontName='Calibri-Bold', fontSize=11, leading=14, textColor=INK, spaceAfter=3, keepWithNext=True),
    'bullet': ParagraphStyle('bullet_hh', fontName='Calibri', fontSize=10.5, leading=13.5, textColor=INK, leftIndent=10, firstLineIndent=-10, spaceAfter=5),
}

EDITS = {
    'RU': {
        'role': 'Python Backend Developer / Python-разработчик',
        'summary': 'Python backend-разработчик с 3 годами опыта в B2B SaaS. Разрабатываю REST API на Django/DRF и FastAPI, оптимизирую PostgreSQL, реализую интеграции и фоновые задачи. Веду изменения от требований и проектирования до релиза и поддержки.',
        'results': [
            '<b>Производительность API:</b> сократил число SQL-запросов к каталогу с <b>74 до 11</b>, p95 времени ответа - с <b>920 до 240 мс</b> при одинаковой нагрузке и данных. Устранил N+1, подобрал индексы с EXPLAIN ANALYZE.',
            '<b>Фоновые задачи и интеграции:</b> вынес длительные операции в Celery/RabbitMQ, настроил тайм-ауты, ограниченные повторы и получение статуса задачи через API. Защитил обработку webhook от дублирования транзакциями и уникальными ключами.',
            '<b>Тестирование:</b> довёл покрытие прикладного backend-кода до <b>87% строк</b> с pytest. Добавил unit- и интеграционные проверки прав доступа, повторных запросов, тайм-аутов и некорректных ответов внешних API.',
            '<b>Выпуск изменений:</b> сократил типовой релиз с <b>40 до 10 минут</b>. Автоматизировал сборку и выпуск через Docker и GitHub Actions, включая тесты, миграции и health checks.',
        ],
        'responsibility': 'Проектировал модели данных, авторизацию и валидацию Pydantic; развивал API на Django/DRF и FastAPI. Работал с Redis, транзакциями и миграциями PostgreSQL, сохранял совместимость схемы и API при обновлениях. Уточнял требования, оценивал задачи, участвовал в code review, разбирал сбои по логам и добавлял регрессионные тесты.',
        'skills': [
            '<b>Backend:</b> Python, Django, Django REST Framework (DRF), FastAPI, asyncio, Pydantic, REST API, HTTP, JWT.',
            '<b>Данные и очереди:</b> PostgreSQL, SQL, Django ORM, SQLAlchemy, Redis, Celery, RabbitMQ.',
            '<b>Тесты и инфраструктура:</b> pytest, unit/integration tests, Git, Linux, Docker, Docker Compose, GitHub Actions, CI/CD.',
            '<b>Дополнительно:</b> JavaScript, React.',
        ],
    },
    'EN': {
        'role': 'Python Backend Developer',
        'summary': 'Python backend developer with 3 years of experience in B2B SaaS. Build REST APIs with Django/DRF and FastAPI, optimize PostgreSQL queries, and implement integrations and background processing. Own changes from requirements and design through release and production support.',
        'results': [
            '<b>API performance:</b> reduced SQL queries per catalog request from <b>74 to 11</b> and p95 latency from <b>920 to 240 ms</b> under the same load and dataset. Removed N+1 queries and tuned indexes using EXPLAIN ANALYZE.',
            '<b>Background processing and integrations:</b> moved long-running operations to Celery/RabbitMQ with timeouts, bounded retries and task-status endpoints. Prevented duplicate webhook processing using transactions and unique keys.',
            '<b>Testing:</b> reached <b>87% line coverage</b> of application backend code with pytest. Added unit and integration tests for access permissions, duplicate requests, timeouts and invalid external API responses.',
            '<b>Release automation:</b> cut typical release time from <b>40 to 10 minutes</b>. Automated builds and releases with Docker and GitHub Actions, including tests, migrations and health checks.',
        ],
        'responsibility': 'Designed data models, authorization and Pydantic validation; developed APIs with Django/DRF and FastAPI. Worked with Redis, PostgreSQL transactions and migrations, preserving schema and API compatibility during updates. Clarified requirements, estimated tasks, reviewed code, investigated failures through logs and added regression tests.',
        'skills': [
            '<b>Backend:</b> Python, Django, Django REST Framework (DRF), FastAPI, asyncio, Pydantic, REST API, HTTP, JWT.',
            '<b>Data and messaging:</b> PostgreSQL, SQL, Django ORM, SQLAlchemy, Redis, Celery, RabbitMQ.',
            '<b>Testing and infrastructure:</b> pytest, unit/integration tests, Git, Linux, Docker, Docker Compose, GitHub Actions, CI/CD.',
            '<b>Additional:</b> JavaScript, React.',
        ],
    },
}

def plain(s):
    return unescape(re.sub('<[^>]+>', '', s.replace('<br/>', '\n')))

def build(lang):
    d, e = DATA[lang], EDITS[lang]
    path = OUT / f'Alexey_Python_Backend_{lang}_Revised.pdf'
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=43, leftMargin=43, topMargin=30, bottomMargin=30,
        title=d['name'] + ' | Python Backend Developer', author=d['name'], subject='Python backend resume')
    story, txt = [], []
    def p(s, style='body'):
        story.append(Paragraph(s, STYLES[style]))
        txt.append(plain(s))
    p(d['name'], 'name')
    p(e['role'], 'role')
    p(d['location'] + ' | ' + link('https://github.com/Middlewarer', 'github.com/Middlewarer'), 'small')
    story.append(Spacer(1, 7))
    p(e['summary'])
    p(d['exp_title'], 'section')
    p(d['job'], 'job')
    p(d['dates'], 'small')
    p(d['scope'])
    for result in e['results']:
        p('- ' + result, 'bullet')
    p('<b>' + d['responsibility_title'] + '.</b> ' + e['responsibility'])
    p(d['skills_title'], 'section')
    for skill in e['skills']:
        p(skill)
    p(d['project_title'], 'section')
    p(d['project_brief'])
    p(link('https://eidosacademy.ru', 'eidosacademy.ru') + ' | ' + link('https://github.com/Middlewarer/EidosAcademy', 'github.com/Middlewarer/EidosAcademy'), 'small')
    p(d['education_title'], 'section')
    p(d['education'])
    doc.build(story)
    reader = PdfReader(path)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    assert len(reader.pages) == 1, (lang, len(reader.pages))
    for required in ('74', '11', '920', '240', '87%', '40', '10', '2023', '2026', 'EidosAcademy'):
        assert required in text, required
    assert d['location'] in text
    for removed in ('Макет:', 'Sample:', 'hypothetical', 'смоделированы', 'Место для фото'):
        assert removed not in text
    (OUT / f'Alexey_Python_Backend_{lang}_Revised.txt').write_text('\n\n'.join(txt) + '\n', encoding='utf-8')
    return {'path': str(path), 'pages': len(reader.pages), 'words': len(text.split()), 'links': len(reader.pages[0].get('/Annots', []))}

if __name__ == '__main__':
    print(json.dumps([build(lang) for lang in ('RU', 'EN')], ensure_ascii=False, indent=2))
