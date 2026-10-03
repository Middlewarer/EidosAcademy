"""Windows real-widget smoke test; isolated state, no network or credentials."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from app import LearningApp, enable_dpi_awareness
from interview_lab import MODES
from daily_plan import build_daily_plan


def main():
    enable_dpi_awareness()
    with tempfile.TemporaryDirectory() as folder:
        state = Path(folder) / "progress.json"
        state.write_text(json.dumps({"learning_model": 6, "completed": ["python-01-p01"],
            "applications": [{"id": "old", "source": "browser", "role": "Archived"}],
            "interview_sessions": [{"date": "2026-09-28", "track_id": "python", "score": 71, "note": "old attempt"}]}))
        root = LearningApp(state)
        failures = []
        root.report_callback_exception = lambda *args: failures.append(str(args[1]))
        root.withdraw()
        assert root.store.data["completed"] == ["python-01-p01"]
        assert root.store.data["start_date"] == "2026-10-02"
        assert len(root.store.data["integration_archive"]["applications"]) == 1
        root.open_applications()
        manual = root.windows["applications"]
        root.update()
        assert not hasattr(manual, "feed_view")
        manual.fields["company"].insert(0, "Fixture")
        manual.fields["role"].insert(0, "Junior")
        manual.add()
        manual.withdraw()
        root.open_interview()
        lab = root.windows["interview"]
        lab.geometry("900x680")
        root.update()
        for index in range(len(MODES)):
            lab.mode.current(index)
            lab.generate()
            assert lab.prompt and "по одному" in lab.prompt
        lab.mode.current(1)
        lab.generate()
        for field in lab.scores:
            field.insert(0, "23")
        lab.questions.insert("1.0", "Объекты и ссылки; изменяемость; тесты краёв")
        lab.notes.insert("1.0", "Независимый пример и проверенный результат: ссылка на код")
        lab.mistakes.insert("1.0", "Ошибка границы списка: исправил и проверил пустой список")
        with patch("interview_lab.messagebox.showinfo"):
            lab.save()
        root.update()
        assert lab.winfo_exists()
        assert len(root.store.data["interview_sessions"]) == 2
        assert root.store.data["interview_sessions"][-1]["qualified"]
        assert len(root.store.data["interview_sessions"][-1]["reviews"]) == 3
        assert not root.store.data["verification_records"]
        with patch("interview_lab.messagebox.showerror") as error:
            lab.save()
            assert error.called, "Saving the same generated attempt twice must be rejected"
        lab.withdraw()
        root.open_plan()
        root.update()
        root.windows["daily-plan"].withdraw()
        specialization = next(d for d in build_daily_plan() if d["phase"]["id"] == "async-specialization")
        with patch("app.calendar_day", return_value=(specialization, None)):
            root.open_today()
            root.update()
        root.destroy()
        assert not failures, failures
        loaded = json.loads(state.read_text(encoding="utf-8"))
        assert loaded["completed"] == ["python-01-p01"]
        assert len(loaded["applications"]) == 1
        assert loaded["interview_sessions"][0]["note"] == "old attempt"
    print("HARD_MODE_GUI_OK: migration, seven modes, scoring, history, manual records, learning-first plan")


if __name__ == "__main__":
    main()
