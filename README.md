# EidosAcademy

Платформа с курсами по программированию на Django и React.

Делаю её как учебный проект: разбираюсь с API, авторизацией, связями в базе и взаимодействием frontend с backend. Курсы разбиты на модули и топики, материалы написаны в Markdown. Контент добавляется через Django Admin.

Проект в разработке. Сейчас можно зарегистрироваться, войти, добавить курс, проходить топики и продолжать с последнего открытого места.

## Что есть

- Каталог с поиском по названию и фильтрами Python / Django.
- Страница курса с программой и списком модулей.
- Просмотр материалов, переключение между топиками и переход к следующему модулю.
- Регистрация по логину и двум паролям, вход через JWT.
- Профиль со статистикой, карточкой курса и достижениями из базы.
- Светлая и тёмная темы с сохранением выбора.
- Адаптивная вёрстка и мобильное меню.
- Админка для управления курсами и материалами.

Посещение топика переводит его в состояние «В процессе», а явная кнопка завершения — в «Пройден». Статусы модулей и курса рассчитываются по дочерним топикам, а полоса показывает долю завершённых топиков во всём курсе.

## Стек

| Часть | Технологии |
| --- | --- |
| Backend | Python, Django 6, Django REST Framework |
| База данных | PostgreSQL |
| Авторизация | Simple JWT |
| Frontend | React 19, React Router, Vite 7 |
| Материалы | react-markdown, remark-gfm |
| Интерфейс | CSS, react-hot-toast |

## Локальный запуск

Нужны Python 3.12+, Node.js 22.12+ и запущенный PostgreSQL. Backend и frontend работают в разных терминалах.

### 1. Backend

Из корня проекта создай виртуальное окружение:

```bash
python -m venv venv
```

Активируй его в Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

В Windows CMD:

```bat
venv\Scripts\activate.bat
```

Или в Linux / macOS:

```bash
source venv/bin/activate
```

Установи зависимости:

```bash
python -m pip install -r requirements.txt
```

Pillow для `ImageField` включён в `requirements.txt`. Для установки `psycopg2` из исходников могут понадобиться инструменты сборки и `pg_config` из PostgreSQL.

### 2. База и окружение

Создай пустую базу через pgAdmin или командой:

```bash
createdb -U postgres EidosAcademy_DB
```

В корне проекта скопируй `.env.example` в `.env`. Заполни все переменные шаблона, включая параметры БД, разрешённые хосты и CORS. Например, для локальной базы:

```dotenv
SECRET_KEY=replace-with-your-generated-key
DEBUG=True
DB_NAME=EidosAcademy_DB
DB_USER=postgres
DB_PASSWORD=your-local-database-password
```

Значения здесь — примеры. Для `SECRET_KEY` можно получить случайный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Файл `.env` не нужно коммитить. Адрес базы задаётся переменными `DB_HOST` и `DB_PORT`. В `ALLOWED_HOSTS` перечисли хосты backend через запятую, без схемы и пути.

Примени миграции, создай администратора и запусти сервер:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Админка: [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### 3. Frontend

Скопируй `frontend/.env.example` в `frontend/.env` и укажи адрес backend в `VITE_API_URL`, без `/api` и завершающего `/`. Во втором терминале:

```bash
cd frontend
npm ci
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Сайт: [127.0.0.1:5173](http://127.0.0.1:5173/).

Порт `5173` указан намеренно: он разрешён в примере CORS-настроек. Если порт занят, освободи его или измени `CORS_ALLOWED_ORIGINS` в корневом `.env`. После изменения `frontend/.env` перезапусти Vite; для production потребуется новая сборка. Переменные `VITE_` видны в браузере, поэтому секреты в них хранить нельзя.

## Первый production-запуск через Docker

На сервере должны быть установлены Docker Engine и Docker Compose. Скопируй `.env.production.example` в `.env.production` и замени домен, пароли и `SECRET_KEY`.

Для локальной проверки оставь:

```dotenv
SITE_ADDRESS=http://localhost
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost
CSRF_TRUSTED_ORIGINS=http://localhost
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

Собери и запусти всю систему:

```bash
docker compose --env-file .env.production up --build -d
docker compose --env-file .env.production exec backend python manage.py createsuperuser
```

Compose запускает PostgreSQL и Redis во внутренней сети, применяет миграции, собирает Django static, запускает backend через Gunicorn, собирает React и публикует приложение через Caddy. PostgreSQL и Redis наружу не открываются.

Проверка состояния:

```bash
docker compose --env-file .env.production ps
docker compose --env-file .env.production logs -f backend caddy
```

Сайт доступен по адресу из `SITE_ADDRESS`, а проверка backend — по `/health/`. Данные PostgreSQL, Redis, static, media и сертификаты Caddy находятся в именованных Docker volumes.

Для production укажи настоящий домен в `SITE_ADDRESS`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` и `CSRF_TRUSTED_ORIGINS`. После первой успешной проверки HTTPS постепенно увеличь `SECURE_HSTS_SECONDS`; не включай preload до проверки всех поддоменов.

Обновление приложения:

```bash
git pull
docker compose --env-file .env.production up --build -d
```

Перед обновлением базы создай резервную копию:

```bash
docker compose --env-file .env.production exec -T db pg_dump -U YOUR_DB_USER YOUR_DB_NAME > backup.sql
```

### 4. Первый курс

Готовой базы с контентом в репозитории нет. После запуска добавь через админку:

1. Категорию.
2. Курс, связанный с категорией.
3. Модуль курса.
4. Топик модуля.
5. Материал `TopicLesson` с Markdown в поле `content`.

Поле `order` задаётся с нуля, без пропусков: `0, 1, 2…` отдельно внутри каждого курса, модуля и топика. Интерфейс сейчас показывает первый материал выбранного топика, поэтому для начала достаточно одного `TopicLesson` на топик.

## Структура

```text
EidosAcademy/
├── backend/                 # Настройки Django и корневые маршруты
├── courses/                 # Модели, API, сериализаторы и миграции
├── frontend/
│   ├── src/
│   │   ├── components/      # Карточки, навигация, API-клиент, AuthContext
│   │   ├── pages/           # Главная, курсы, модули, профиль, вход
│   │   └── styles/          # Стили страниц и обе темы
│   └── package.json
├── manage.py
└── requirements.txt
```

## Полезные команды

В корне проекта, с активированным виртуальным окружением:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

В папке `frontend`:

```bash
npm run dev       # Локальная разработка
npm run build     # Сборка в frontend/dist
npm run preview   # Локальный просмотр сборки
npm run lint      # Проверка JavaScript и React
```

## Дальше

- [x] Закончить запись на курс и сохранение завершённых топиков.
- [x] Запоминать последний открытый топик и продолжать с него обучение.
- [ ] Показывать реальные события в профиле вместо статических примеров.
- [ ] Добавить понятные состояния загрузки, ошибок и пустых списков.
- [ ] Закрыть права на изменение учебных материалов через API.
- [x] Покрыть регистрацию и прогресс основными тестами.
- [ ] Подготовить конфигурацию для деплоя.

Текущие настройки рассчитаны на локальную разработку, не на публичный сервер. Перед публикацией нужно настроить домены и HTTPS, выключить debug, вынести адреса API и базы в окружение и проверить права доступа. `npm run build` собирает только frontend — сам по себе он не разворачивает Django и PostgreSQL.

## Авторизация

Все защищённые запросы используют `apiRequest`: при 401 клиент один раз обновляет токены и повторяет запрос. Одновременные запросы между вкладками разделяют обновление через Web Locks. Для этого нужен современный браузер и HTTPS либо localhost. Обновление токенов не сбрасывает профиль в соседних вкладках; вход, выход и смена аккаунта синхронизируются отдельно. Вход и регистрация не запускают refresh. Временные ошибки сети и сервера не удаляют токены.

Выход отзывает текущий refresh через `POST /api/logout/`, затем очищает состояние браузера. Уже выданный access при обычном выходе действителен до истечения его срока (30 минут). После смены пароля все ранее выданные access и refresh отклоняются; требуется повторный вход. Старые токены, выданные до включения проверки смены пароля, также требуют повторного входа.

Перед запуском примените `python manage.py migrate`: необходимы таблицы `token_blacklist`. Периодически запускайте `python manage.py flushexpiredtokens` для очистки истёкших записей.

Для самостоятельной работы оставлено ограничение частоты входа, регистрации и смены пароля. Сейчас для них лимиты не включены. Для refresh сохранён лимит 60/мин, для выхода — 30/мин. DRF throttling использует кеш; для нескольких серверных процессов при деплое нужен общий кеш. Это ограничение частоты на уровне приложения, а не защита от DDoS.

Проверки: `python manage.py test courses.tests`, `npm --prefix frontend test`, `npm --prefix frontend run lint`, `npm --prefix frontend run build`.
