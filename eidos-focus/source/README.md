# Eidos Focus — первый этап нового Eidos Tracker

Современное desktop-приложение Windows для существующего `progress.json`. React/TypeScript работает внутри отдельного нативного окна на системном WebView2; внешний браузер и Tkinter не используются.

## Что уже работает

- startup dashboard с тремя действиями на день;
- контракт дня: результат, дедлайн, объём фокуса и ожидаемое отвлечение;
- focus timer 50 минут с записью времени в старый `work_seconds`;
- завершённые сессии увеличивают старый `pomodoro_sessions`;
- streak, heatmap, фокус за день и карьерные показатели;
- быстрый учёт отклика в существующем массиве `applications`;
- обзор учебных треков, резюме и интервью;
- чтение `CURRICULUM`, если рядом доступен `mastery_curriculum.py`;
- атомарное сохранение, проверка конфликтов и резервные копии.

## Запуск

1. Дважды щёлкните `app\Eidos Focus.exe` или ярлык Eidos Focus на рабочем столе.
2. Откроется отдельное окно Windows `Eidos Focus`. Внешний браузер не используется.

Для запуска вместе с Windows один раз выполните `powershell -ExecutionPolicy Bypass -File .\install-autostart.ps1`.

По умолчанию используется `%USERPROFILE%\.eidos_learning_tracker\progress.json` — тот же путь, что и в исходном `app.py`.

Для другого файла:

```powershell
$env:EIDOS_STATE_FILE = "D:\path\to\progress.json"
.\run.ps1
```

Чтобы загрузить точные названия и объём учебных треков, укажите каталог старого проекта:

```powershell
$env:EIDOS_LEGACY_DIR = "D:\path\to\eidos-tracker"
.\run.ps1
```

## Совместимость данных

Существующие ключи не удаляются и не переименовываются. Новые сущности находятся только в `focus_os`:

```json
{
  "focus_os": {
    "version": 1,
    "daily_missions": {},
    "commitments": {},
    "focus_sessions": [],
    "parking_lot": {}
  }
}
```

Перед первой записью создаётся `progress.before_eidos_focus.json`, а перед каждой следующей — `progress.last-good.json`.

## Практичная архитектура миграции

Сейчас: `React UI → локальный HTTP API → совместимый progress.json`. Это позволяет сразу заменить визуальный слой, не переписывая и не рискуя всей предметной логикой.

Следующий этап: поместить frontend в Tauri, добавить system tray/autostart/мини-виджет, а Python-мост запускать sidecar-процессом. После стабилизации схемы бизнес-логику можно постепенно перенести в Rust/TypeScript. Для сборки Tauri потребуется установить Rust; в текущей системе он не обнаружен.
