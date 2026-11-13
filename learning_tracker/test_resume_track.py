import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import Store
from career_readiness import readiness_summary
from mastery_curriculum import CURRICULUM
from resume_track import STEPS, STAGES, complete, export_report, make_record, prompt, summary


class ResumeTrackTests(unittest.TestCase):
    def values(self, **changes):
        return dict(understood=True, practiced=True, reported=True,
                    evidence="tests/test_api.py: три сценария прошли, чужой объект недоступен",
                    report="Задача: ограничить доступ. Изменил queryset и проверил два аккаунта.",
                    gaps="Повторить истечение токена", origin="Учебная симуляция") | changes

    def test_curriculum_covers_resume_and_workflow_with_resolvable_base_tracks(self):
        self.assertEqual(len({s['id'] for s in STEPS}), 20)
        ids = {s['id'] for s in STEPS}
        self.assertTrue({'context', 'ticket', 'review', 'api', 'auth', 'orm', 'migration',
                         'queries', 'cache', 'external', 'celery', 'webhook', 'fastapi',
                         'pytest', 'frontend', 'docker', 'release', 'incident', 'defense'} <= ids)
        tracks = {t['id'] for t in CURRICULUM}
        for s in STEPS:
            self.assertTrue(set(s['tracks']) <= tracks)
            self.assertGreaterEqual(len(s['acceptance']), 3)
            self.assertGreaterEqual(len(s['questions']), 3)
            self.assertTrue(s['ticket'] and s['claim'] and s['learn'])

    def test_partial_records_cannot_complete_without_practice_and_report(self):
        for stage, _ in STAGES:
            self.assertFalse(complete(self.values(**{stage: False})))
        for missing in ('evidence', 'report'):
            with self.assertRaises(ValueError):
                make_record('api', {}, self.values(**{missing: ' '}))
        self.assertFalse(complete(make_record('api', {}, self.values(practiced=False, evidence=''))))
        self.assertTrue(complete(make_record('api', {}, self.values())))
        with self.assertRaises(ValueError):
            make_record('wrong', {}, self.values())

    def test_old_progress_preserved_and_new_history_survives_reload(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Store(Path(folder) / 'progress.json')
            store.data['completed'] = ['python-01-p01']
            store.data['career_profile'] = {'resume_text': 'Существующий текст'}
            store.data['project_records'] = {'keep': {'evidence': 'old'}}
            store.save()
            old = copy.deepcopy(store.data)
            metrics = readiness_summary(store)
            store.save_resume_step('api', self.values())
            self.assertEqual(readiness_summary(store), metrics)
            store.save_resume_step('api', self.values(reported=False, report='Нужна ещё одна попытка'))
            loaded = Store(store.path)
            for key in old:
                self.assertEqual(loaded.data[key], old[key], key)
            rec = loaded.data['resume_track']['records']['api']
            self.assertEqual(len(rec['attempts']), 2)
            self.assertTrue(rec['attempts'][0]['reported'])
            self.assertFalse(rec['reported'])
            self.assertEqual(summary(loaded.data)['done'], 0)

    def test_failed_save_rolls_back_memory_and_conflict_preserves_other_writer(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Store(Path(folder) / 'progress.json')
            store.save()
            before = copy.deepcopy(store.data)
            with patch.object(store, 'save', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    store.save_resume_step('context', self.values())
            self.assertEqual(store.data, before)
            other = Store(store.path)
            other.save_resume_step('api', self.values())
            with self.assertRaises(RuntimeError):
                store.save_resume_step('context', self.values())
            self.assertEqual(store.data, before)
            persisted = Store(store.path)
            self.assertIn('api', persisted.data['resume_track']['records'])
            self.assertNotIn('context', persisted.data['resume_track']['records'])

    def test_next_step_and_export_keep_origin_and_actual_notes(self):
        data = {'resume_track': {'records': {}}}
        for item in STEPS:
            data['resume_track']['records'][item['id']] = make_record(item['id'], {}, self.values())
        self.assertEqual(summary(data)['done'], 20)
        self.assertIsNone(summary(data)['next_id'])
        data['resume_track']['records']['webhook']['reported'] = False
        self.assertEqual(summary(data)['next_id'], 'webhook')
        report = export_report(data)
        self.assertIn('19 / 20', report)
        self.assertIn('Учебная симуляция', report)
        self.assertIn(self.values()['evidence'], report)
        for mode in ('learn', 'interview'):
            text = prompt(STEPS[0], mode, self.values())
            self.assertIn('по одному', text)
            self.assertIn(self.values()['gaps'], text)
            self.assertIn('Не придумывай работодателей', text)


if __name__ == '__main__':
    unittest.main()
