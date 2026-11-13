# Разбор исходного Eidos Tracker и план миграции

## Что было доступно

Во вложении присутствовал только `app.py` (115 065 байт). Соседние модули, которые он импортирует, в каталоге вложения отсутствовали:

- `daily_plan.py` — `TRACK_PRIORITY`, `build_daily_plan`;
- `career_readiness.py` — проекты, резюме, проверка знаний и итоговая готовность;
- `manual_applications.py` — окно откликов;
- `preparation.py` — дисциплина, миграция, checkpoints;
- `interview_lab.py` — интервью;
- `mastery_curriculum.py` — `CURRICULUM`, `all_task_ids`;
- `progress_insights.py` — календарь, долги, недельная статистика;
- `resume_track.py` — пошаговый трек резюме.

Точка входа: `LearningApp().mainloop()` в конце `app.py`. Текущий UI — Tkinter. Данные по умолчанию находятся в `%USERPROFILE%\.eidos_learning_tracker\progress.json`, путь можно переопределить через `EIDOS_STATE_FILE`.

## Подтверждённая схема progress.json

`Store.load()` устанавливает и использует следующие ключи:

| Ключ | Тип | Назначение |
|---|---|---|
| `learning_model` | number | текущая модель обучения, в исходнике `6` |
| `career_model` | number | текущая карьерная модель, в исходнике `1` |
| `completed` | string[] | решённые задания |
| `prompt_ready` | string[] | пройденные вводные промпты |
| `task_records` | object | статусы, заметки, пути и история попыток |
| `work_seconds` | object | секунды фокуса по ISO-дате |
| `pomodoro_sessions` | object | завершённые сессии по ISO-дате |
| `daily_target_hours` | number | дневная цель |
| `pomodoro_preset` | string | `50/10` или `25/5` |
| `interview_sessions` | array | история интервью |
| `daily_quests` | object | выполненные дневные проверки |
| `career_actions` | object | выполненные карьерные действия |
| `verification_records` | object | проверки тем и evidence |
| `applications` | array | отклики: id, company, role, url, status, note, timestamps |
| `project_records` | object | evidence проектных milestones |
| `career_profile` | object | карьерный профиль |
| `resume_checklist` | object | готовность резюме |
| `resume_track` | object | отдельная версия и records трека резюме |

Исходный Store уже применяет полезные гарантии: SHA-256 проверку конкурентной записи, `progress.last-good.json`, однократный backup и атомарную замену временного файла. Новый мост повторяет эти гарантии и не вызывает старую миграцию, чтобы не менять данные неявно.

## Выбранная архитектура

```text
React + TypeScript inside native Windows WebView2
        ↓ local-only JSON API
packaged Python desktop host
        ↓ atomic, compatible writes
existing progress.json
```

Пользователь видит отдельное окно Windows, а не браузер. WebView2 используется как системный движок отрисовки современного интерфейса. Старый Tkinter Eidos может продолжать работать с тем же файлом. Новые поля изолированы в `focus_os`; неизвестные поля сохраняются.

## Путь к desktop-версии

1. Подложить в этот проект полный старый каталог и проверить точный `CURRICULUM`.
2. Обернуть собранный frontend в Tauri 2.
3. Запускать Python bridge как sidecar; добавить tray, автозапуск и компактное окно таймера.
4. После стабилизации API переносить отдельные расчёты из Python в Rust/TypeScript, оставляя миграционные тесты на реальных копиях `progress.json`.

Rust toolchain в текущей среде не установлен, поэтому первый этап намеренно остаётся запускаемым сейчас, а не непроверенным Tauri-скелетом.
