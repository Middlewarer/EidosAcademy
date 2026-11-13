"""Real-widget regression check with isolated state and no real user data."""
import tempfile
from pathlib import Path
from unittest.mock import patch
from app import LearningApp, Store, enable_dpi_awareness
import resume_track


def main():
    enable_dpi_awareness()
    with tempfile.TemporaryDirectory() as folder:
        state = Path(folder) / 'progress.json'
        root = LearningApp(state)
        root.withdraw()
        errors = []
        root.report_callback_exception = lambda *args: errors.append(str(args[1]))
        root.open_resume_track()
        window = root.windows['resume-track']
        window.geometry('940x660')
        root.update()
        assert window.index == 0
        for index in range(len(resume_track.STEPS)):
            window.select(index)
            root.update()
            assert window.item == resume_track.STEPS[index]
            assert all(w.winfo_exists() for w in window.fields.values())
            assert all(w.winfo_width() > 350 for w in window.fields.values())
        window.select(0)
        window.fields['report'].insert('1.0', 'Черновик: схема сервиса и мой личный вклад.')
        window.select(1)  # Navigation saves the draft.
        assert Store(state).data['resume_track']['records']['context']['report'].startswith('Черновик')
        window.select(0)
        window.checks['practiced'].set(True)
        with patch('app.messagebox.showerror') as error:
            window.select(1)
            assert error.called
            assert window.index == 0
        window.fields['evidence'].insert('1.0', 'docs/context.md: схема запроса и роли проверены по примеру.')
        for var in window.checks.values():
            var.set(True)
        window.save()
        assert resume_track.summary(root.store.data)['done'] == 1
        window.next_step()
        assert window.index == 1
        output = Path(folder) / 'report.md'
        with patch('app.filedialog.asksaveasfilename', return_value=str(output)):
            window.export()
        assert '1 / 20' in output.read_text(encoding='utf-8')
        window.close()
        root.open_resume_track()
        reopened = root.windows['resume-track']
        assert reopened.index == 1
        reopened.fields['gaps'].insert('1.0', 'Вспомнить порядок передачи задачи в QA.')
        root.destroy()  # Closing the parent must save an open draft too.
        loaded = Store(state)
        assert loaded.data['resume_track']['records']['ticket']['gaps'].startswith('Вспомнить')
        assert not loaded.data['completed']
        assert not errors, errors
    print('RESUME_TRACK_GUI_OK: 20 steps, draft navigation, validation, persistence, export, parent close')


if __name__ == '__main__':
    main()
