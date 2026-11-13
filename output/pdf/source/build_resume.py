from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

OUT = Path(__file__).resolve().parents[1]
for name, file in [('Calibri','calibri.ttf'),('Calibri-Bold','calibrib.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path(r'C:\Windows\Fonts')/file)))
pdfmetrics.registerFontFamily('Calibri',normal='Calibri',bold='Calibri-Bold')
W,H=A4
BLUE,INK,MUTED='#245478','#202B36','#576474'
base=dict(fontName='Calibri',fontSize=11,leading=15.2,textColor=HexColor(INK))
styles={
    'body':ParagraphStyle('body',**base),
    'small':ParagraphStyle('small',**(base|dict(fontSize=10.3,leading=13.8,textColor=HexColor(MUTED)))),
    'skills':ParagraphStyle('skills',**(base|dict(fontSize=10.6,leading=14.5))),
    'job':ParagraphStyle('job',**(base|dict(fontName='Calibri-Bold',fontSize=12,leading=16.5))),
    'sub':ParagraphStyle('sub',**(base|dict(fontName='Calibri-Bold',fontSize=11.3,leading=15.5))),
    'section':ParagraphStyle('section',**(base|dict(fontName='Calibri-Bold',fontSize=13,leading=18,textColor=HexColor(BLUE)))),
    'name':ParagraphStyle('name',**(base|dict(fontName='Calibri-Bold',fontSize=27,leading=32))),
    'role':ParagraphStyle('role',**(base|dict(fontName='Calibri-Bold',fontSize=16,leading=22,textColor=HexColor(BLUE)))),
}
def link(url,label):return f'<link href="{url}" color="{BLUE}">{label}</link>'

DATA={
'RU':{
 'name':'Алексей','role':'Python-разработчик','location':'Кострома, Россия | Удалённая работа',
 'summary':'Разрабатываю серверную часть веб-приложений на Python. Основные задачи: REST API, интеграции, PostgreSQL и фоновые операции. Веду изменения от оценки и проектирования до релиза и поддержки.',
 'skills_title':'Технические навыки',
 'skills':[
 '<b>Языки:</b> Python; JavaScript для интерфейсов на React.',
 '<b>Backend:</b> Django, Django REST Framework, FastAPI, asyncio, Pydantic.',
 '<b>Данные:</b> PostgreSQL, SQL, Django ORM, SQLAlchemy, Redis.',
 '<b>Интеграции:</b> REST API, HTTP, JWT, Celery, RabbitMQ.',
 '<b>Тестирование:</b> pytest, unit- и интеграционные тесты, моки внешних сервисов.',
 '<b>Инфраструктура:</b> Git, Linux, Docker, Docker Compose, GitHub Actions, CI/CD.',
 ],
 'exp_title':'Опыт работы',
 'job':'Python-разработчик | Продуктовая компания, B2B SaaS',
 'dates':'Сентябрь 2023 - сентябрь 2026 | 3 года',
 'scope':'Платформа с личными кабинетами, управлением доступом и интеграциями. Отвечал за backend-функции, взаимодействие с внешними сервисами и сопровождение выпущенных изменений.',
 'responsibility_title':'Зона ответственности',
 'responsibilities':[
 'Проектировал и развивал API на <b>Django/DRF и FastAPI</b>: модели данных, валидация Pydantic, авторизация и асинхронные запросы к внешним сервисам.',
 'Работал с <b>PostgreSQL и Redis</b>: SQL-запросы, индексы, транзакции, миграции, кэширование и обновление данных в кэше.',
 'Уточнял требования, оценивал задачи, участвовал в code review. Разбирал ошибки по логам, добавлял проверки и документировал поведение API.',
 ],
 'results_title':'Основные результаты',
 'results':[
 'Устранил N+1 и подобрал индексы через EXPLAIN ANALYZE. Для запроса каталога сократил число SQL-запросов <b>с 74 до 11</b>, p95 времени ответа - <b>с 920 до 240 мс</b> при одинаковой нагрузке и данных.',
 'Реализовал фоновые операции на <b>Celery/RabbitMQ</b>: повторные попытки, тайм-ауты и обработку ошибок. Защитил webhook от повторного выполнения через транзакции и уникальные ключи.',
 'Довёл покрытие прикладного backend-кода до <b>87% строк</b> с pytest. Добавил проверки прав доступа, повторных запросов, тайм-аутов и некорректных ответов внешнего API.',
 'Автоматизировал сборку и выпуск через <b>Docker и GitHub Actions</b>: тесты, миграции и health checks. Сократил время типового релиза <b>с 40 до 10 минут</b>.',
 ],
 'details_title':'Опыт работы: технические задачи',
 'work_groups':[
 ('Интеграции и фоновые задачи',[
 'Выносил длительные операции из API в Celery. Сохранял состояние задачи в PostgreSQL, чтобы клиент мог получить статус и результат обработки отдельным запросом.',
 'Настраивал тайм-ауты и ограниченное число повторных попыток. Разделял временные сбои внешнего сервиса и ошибки входных данных, которые повторять бессмысленно.',
 'Сохранял идентификатор внешнего события и статус его обработки. Изменение доступа пользователя и фиксацию результата выполнял в одной транзакции.',
 ]),
 ('Данные и совместимость изменений',[
 'Поддерживал схемы данных через миграции. Разделял добавление новых полей, пакетное заполнение данных и удаление устаревших полей, сохраняя совместимость с работающей версией приложения.',
 'Проверял границы транзакций и ограничения уникальности в сценариях параллельных запросов. Оптимизировал выборки по планам выполнения, а не только по времени ответа API.',
 'Документировал форматы запросов, коды ошибок и изменения контрактов. Согласовывал доработки API с клиентской частью до выпуска обновления.',
 ]),
 ('Проверка и сопровождение релизов',[
 'Писал unit-тесты бизнес-логики и интеграционные тесты с PostgreSQL. Для внешних API воспроизводил сетевые ошибки, тайм-ауты, повторные события и некорректный JSON.',
 'Разбирал сбои по логам API и фоновых задач. После исправления добавлял регрессионную проверку и обновлял документацию; проверял миграции и доступность сервиса после релиза.',
 ]),
 ],
 'project_title':'Личный проект',
 'project_brief':'<b>EidosAcademy.</b> Образовательная платформа на Django/DRF, PostgreSQL и React. Разработал API, авторизацию и учёт прогресса; настроил тесты, CI и развёртывание.',
 'education_title':'Образование',
 'education':'<b>Костромской государственный университет</b><br/>Информационные системы и технологии | Бакалавриат, 3-й курс',
 'footer':'Макет: коммерческий опыт, часть навыков и показатели эффективности смоделированы.',
},
'EN':{
 'name':'Alexey','role':'Python Backend Developer','location':'Bălți, Moldova | Remote',
 'summary':'Python backend developer working on REST APIs, service integrations, PostgreSQL and background processing. Own features from requirements and design through implementation, release and production support.',
 'skills_title':'Technical skills',
 'skills':[
 '<b>Languages:</b> Python; JavaScript for React interfaces.',
 '<b>Backend:</b> Django, Django REST Framework, FastAPI, asyncio, Pydantic.',
 '<b>Data:</b> PostgreSQL, SQL, Django ORM, SQLAlchemy, Redis.',
 '<b>Integrations:</b> REST APIs, HTTP, JWT, Celery, RabbitMQ.',
 '<b>Testing:</b> pytest, unit and integration tests, mocking external services.',
 '<b>Infrastructure:</b> Git, Linux, Docker, Docker Compose, GitHub Actions, CI/CD.',
 ],
 'exp_title':'Experience',
 'job':'Python Backend Developer | B2B SaaS Company',
 'dates':'September 2023 - September 2026 | 3 years',
 'scope':'A platform with user accounts, access management and external integrations. Responsible for backend features, service integrations and support for released functionality.',
 'responsibility_title':'Responsibilities',
 'responsibilities':[
 'Designed and developed APIs with <b>Django/DRF and FastAPI</b>, including data models, Pydantic validation, authorization and asynchronous requests to external services.',
 'Worked with <b>PostgreSQL and Redis</b> on SQL queries, indexing, transactions, schema migrations, caching and cache invalidation.',
 'Clarified requirements, estimated tasks and participated in code reviews. Investigated failures through logs, added regression tests and documented API behavior.',
 ],
 'results_title':'Selected results',
 'results':[
 'Removed N+1 queries and tuned indexes using EXPLAIN ANALYZE. Reduced SQL queries per catalog request <b>from 74 to 11</b> and p95 latency <b>from 920 to 240 ms</b> with the same dataset and load.',
 'Implemented background processing with <b>Celery/RabbitMQ</b>, retries, timeouts and error handling. Prevented duplicate webhook processing using transactions and unique keys.',
 'Reached <b>87% line coverage of application backend code</b> with pytest. Tested access permissions, duplicate requests, timeouts and invalid external API responses.',
 'Automated builds and releases with <b>Docker and GitHub Actions</b>, including tests, migrations and health checks. Cut release time <b>from 40 to 10 minutes</b>.',
 ],
 'details_title':'Experience: technical scope',
 'work_groups':[
 ('Integrations and background processing',[
 'Moved long-running operations from API handlers into Celery tasks. Stored task state in PostgreSQL so clients could retrieve processing status and results through a separate endpoint.',
 'Configured timeouts and bounded retries. Distinguished transient service failures from invalid input that would not benefit from another attempt.',
 'Stored external event identifiers and processing status. Applied access changes and recorded their outcome within the same database transaction.',
 ]),
 ('Data and backward compatibility',[
 'Maintained database schemas through migrations. Separated new fields, batched data backfills and removal of obsolete fields to preserve compatibility with the running application.',
 'Reviewed transaction boundaries and uniqueness constraints for concurrent requests. Used query execution plans to investigate performance alongside API response times.',
 'Documented request formats, error codes and contract changes. Coordinated API updates with frontend changes before release.',
 ]),
 ('Testing and release support',[
 'Wrote unit tests for business logic and integration tests against PostgreSQL. Simulated network failures, timeouts, duplicate events and invalid JSON from external APIs.',
 'Investigated failures using API and worker logs. Added regression checks and updated documentation after fixes; verified migrations and service health after releases.',
 ]),
 ],
 'project_title':'Personal project',
 'project_brief':'<b>EidosAcademy.</b> A learning platform built with Django/DRF, PostgreSQL and React. Implemented APIs, authentication and progress tracking; configured tests, CI and deployment.',
 'education_title':'Education',
 'education':'<b>Kostroma State University</b><br/>Information Systems and Technologies | Bachelor\'s degree in progress, third year',
 'footer':'Sample: employment history, some skills and performance figures are hypothetical.',
}}

class Resume:
 def __init__(self,lang):
    self.lang,self.d=lang,DATA[lang]
    self.path=OUT/f'Alexey_Python_Backend_{lang}.pdf'
    self.c=canvas.Canvas(str(self.path),pagesize=A4,pageCompression=1)
    self.c.setTitle(self.d['name']+' - '+self.d['role'])
    self.c.setAuthor(self.d['name'])
    self.c.setSubject('Sample resume with hypothetical commercial experience')
    self.y=35
    self.bottoms=[]
 def p(self,text,style='body',after=0,x=43,width=None):
    p=Paragraph(text,styles[style]);_,h=p.wrap(width or W-86,H)
    p.drawOn(self.c,x,H-self.y-h);self.y+=h+after
 def section(self,text):
    self.y+=12;self.p(text,'section',6)
 def sub(self,text):
    self.y+=8;self.p(text,'sub',5)
 def bullet(self,text):
    self.c.setFillColor(HexColor(BLUE));self.c.circle(46,H-self.y-7.5,1.4,stroke=0,fill=1)
    self.p(text,x=56,width=W-99,after=6)
 def footer(self,n):
    assert self.y<786,(self.lang,n,self.y)
    self.bottoms.append(round(self.y,1))
    self.c.setLineWidth(.5);self.c.setStrokeColor(HexColor('#DCE2E7'))
    self.c.line(43,36,W-43,36)
    self.c.setFillColor(HexColor(MUTED));self.c.setFont('Calibri',8)
    self.c.drawString(43,23,self.d['footer'])
    self.c.drawRightString(W-43,23,f'{n} / 2')
 def header(self):
    d=self.d;hw=W-86-105 if self.lang=='RU' else W-86
    self.p(d['name'],'name',4,width=hw);self.p(d['role'],'role',7,width=hw)
    self.p(d['location'],'small',3,width=hw)
    self.p(link('https://github.com/Middlewarer','github.com/Middlewarer'),'small',width=hw)
    if self.lang=='RU':
      x,top,pw,ph=W-43-85,38,85,103
      self.c.setLineWidth(.7);self.c.setStrokeColor(HexColor('#B5C2CB'));self.c.setFillColor(HexColor('#F7F9FA'))
      self.c.rect(x,H-top-ph,pw,ph,fill=1,stroke=1)
      self.c.setFillColor(HexColor(MUTED));self.c.setFont('Calibri',9)
      self.c.drawCentredString(x+pw/2,H-top-ph/2,'Место для фото')
      self.y=max(self.y,top+ph)
    self.y+=13
 def build(self):
    d=self.d;self.header();self.p(d['summary'])
    self.section(d['skills_title'])
    for line in d['skills']:self.p(line,'skills')
    self.section(d['exp_title']);self.p(d['job'],'job',3);self.p(d['dates'],'small',6);self.p(d['scope'])
    self.sub(d['responsibility_title'])
    for line in d['responsibilities']:self.bullet(line)
    self.sub(d['results_title'])
    for line in d['results']:self.bullet(line)
    self.footer(1);self.c.showPage();self.y=32
    self.p(d['name']+' | '+d['role'],'small',9)
    self.c.setStrokeColor(HexColor('#DCE2E7'));self.c.setLineWidth(.5);self.c.line(43,H-self.y,W-43,H-self.y)
    self.y+=3;self.section(d['details_title']);self.p(d['job'],'small',3)
    for title,items in d['work_groups']:
      self.sub(title)
      for line in items:self.bullet(line)
    self.section(d['education_title']);self.p(d['education'],'small')
    self.section(d['project_title']);self.p(d['project_brief'],'small',4)
    self.p(link('https://eidosacademy.ru','eidosacademy.ru')+' | '+link('https://github.com/Middlewarer/EidosAcademy','github.com/Middlewarer/EidosAcademy'),'small')
    self.footer(2);self.c.save()
    r=PdfReader(self.path);assert len(r.pages)==2
    texts=[p.extract_text() for p in r.pages];alltext='\n'.join(texts)
    assert d['location'] in texts[0]
    assert '87%' in texts[0]
    assert 'EidosAcademy' not in texts[0] and 'eidosacademy.ru' not in texts[0]
    assert texts[1].index(d['education_title']) < texts[1].index('EidosAcademy')
    assert d['education_title'] in texts[1]
    assert ' | Middle' not in alltext and 'Mid-level' not in alltext
    if self.lang=='EN':assert 'Kostroma, Russia' not in alltext and 'Место для фото' not in alltext
    else:assert 'Место для фото' in alltext
    for page in r.pages:
      for ref in page['/Resources']['/Font'].values():
        font=ref.get_object();desc=font.get('/FontDescriptor')
        if desc:assert '/FontFile2' in desc.get_object()
    return {'file':str(self.path),'pages':len(r.pages),'words':[len(t.split()) for t in texts],'body_bottoms':self.bottoms}

if __name__=='__main__':
 print(json.dumps([Resume(lang).build() for lang in ('RU','EN')],ensure_ascii=False,indent=2))
