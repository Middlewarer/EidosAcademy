"""Launch the tracker with a single-writer lock and visible startup errors."""
import argparse
import ctypes
import os
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", action="store_true")
    parser.add_argument("--demo", action="store_true", help="Use isolated temporary data")
    args = parser.parse_args()
    demo = tempfile.TemporaryDirectory(prefix="eidos-demo-") if args.demo else None
    state_path = Path(demo.name) / "progress.json" if demo else Path.home() / ".eidos_learning_tracker" / "progress.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lock = (state_path.parent / "app.lock").open("a+b")
    try:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            if not lock.read(1):
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                ctypes.windll.user32.MessageBoxW(None, "Job Search OS уже запущен. Переключись в открытое окно.", "Job Search OS", 0)
                return
        from app import LearningApp, enable_dpi_awareness
        enable_dpi_awareness()
        root = LearningApp(state_path)
        if not args.demo and root.store.needs_preparation_save:
            import shutil
            backup = state_path.with_name("progress.before_hard_mode.json")
            if state_path.exists() and not backup.exists():
                shutil.copy2(state_path, backup)
            root.store.save()
        if args.demo:
            root.title("Job Search OS · DEMO")
            root.store.data["applications"] = [
                {"id": "demo-1", "company": "Пример · продуктовая команда", "role": "Junior Python Backend Developer",
                 "status": "planned", "url": "", "description": "Python, Django, SQL. Разработка API и тестирование.", "note": "Подготовить рассказ о проекте"},
                {"id": "demo-2", "company": "Пример · сервисная компания", "role": "Python разработчик", "status": "screening",
                 "submitted_at": "2026-09-29", "note": "Подготовить рассказ о проекте", "next_action_at": "2026-10-02"}]
            root.store.data["career_profile"]["letter_facts"] = "Учебный проект: API заказов с интеграционными тестами."
        if args.jobs:
            root.open_applications()
            if args.demo:
                root.withdraw()
                root.windows["applications"].protocol("WM_DELETE_WINDOW", root.destroy)
        root.mainloop()
    except Exception as exc:
        if os.name == "nt":
            ctypes.windll.user32.MessageBoxW(None, str(exc), "Job Search OS — ошибка запуска", 0x10)
        raise
    finally:
        lock.close()
        if demo:
            demo.cleanup()


if __name__ == "__main__":
    main()
