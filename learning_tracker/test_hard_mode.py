import copy
import tempfile
import unittest
from datetime import date
from pathlib import Path

from preparation import migrate, START, discipline
from daily_plan import build_daily_plan
from interview_lab import make_session, build_prompt, MODES
from mastery_curriculum import CURRICULUM
from app import Store


class HardModeTests(unittest.TestCase):
    def test_migration_is_idempotent_and_preserves_learning_and_manual_records(self):
        old = {"completed": ["python-01-p01"], "task_records": {"a": {"attempts": [1, 2]}},
               "start_date": "2026-09-28", "daily_target_hours": 8, "interview_sessions": [{"score": 77}],
               "career_profile": {"resume_text": "Keep me"}, "verification_records": {"a": {"score": 81}},
               "hh_sync": {"last_sync": "old"}, "applications": [
                   {"id": "remote", "source": "browser", "cover_letter": "Keep my letter"},
                   {"id": "manual", "company": "Local", "status": "sent"}]}
        before = copy.deepcopy(old)
        self.assertTrue(migrate(old))
        for key in ("completed", "task_records", "interview_sessions", "career_profile", "verification_records"):
            self.assertEqual(old[key], before[key])
        self.assertEqual(old["applications"], [before["applications"][1]])
        self.assertEqual(old["integration_archive"]["applications"], [before["applications"][0]])
        self.assertEqual(old["start_date"], START.isoformat())
        migrated = copy.deepcopy(old)
        self.assertFalse(migrate(old))
        self.assertEqual(old, migrated)

    def test_plan_has_buffer_and_never_drops_topics(self):
        plan = build_daily_plan()
        core = [d for d in plan if d["phase"]["id"] == "working-backend"]
        self.assertLessEqual(core[-1]["date"], date(2026, 11, 30))
        self.assertLessEqual(plan[-1]["date"], date(2026, 12, 15))
        self.assertTrue(all(d["topics"] for d in plan))
        self.assertTrue(all(15 <= d["career_minutes"] <= 30 for d in plan))
        self.assertTrue(all(d["minutes"] == 540 for d in plan))
        self.assertEqual(len({t["id"] for d in plan for _, t in d["topics"]}), 240)

    def session(self, **changes):
        values = dict(mode="technical", track_id="python", scores=[23, 23, 23, 23], note="Evidence from answer and code",
                      questions="Hash vs equality, list aliasing", mistakes="Mutable default: fix and retest", assisted=False,
                      critical=False, today=START)
        return make_session(**(values | changes))

    def test_scoring_and_retries(self):
        session = self.session()
        self.assertTrue(session["qualified"])
        self.assertEqual(session["score"], 92)
        self.assertEqual([r["due"] for r in session["reviews"]], ["2026-10-03", "2026-10-05", "2026-10-09"])
        for options in ({"assisted": True}, {"critical": True}, {"mode": "diagnostic"}, {"scores": [25, 25, 25, 17]}):
            self.assertFalse(self.session(**options)["qualified"])
        self.assertFalse(self.session(mistakes="")["reviews"])
        for options in ({"scores": [26, 20, 20, 20]}, {"questions": ""}, {"note": ""}):
            with self.assertRaises(ValueError):
                self.session(**options)

    def test_distinct_prompts_include_history_and_do_not_require_verified_topics(self):
        prompts = [build_prompt(m, CURRICULUM[0], [], "", "prior mechanism", "specific error") for m in MODES]
        self.assertEqual(len(set(prompts)), 7)
        for prompt in prompts:
            self.assertIn("prior mechanism", prompt)
            self.assertIn("specific error", prompt)
            self.assertIn("по одному", prompt)
            self.assertIn("Максимум одно уточнение", prompt)
            self.assertIn("опыта работы нет", prompt)

    def test_persistence_does_not_create_verifications(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Store(Path(folder) / "progress.json")
            store.data["interview_sessions"].append(self.session())
            store.save()
            loaded = Store(store.path)
            self.assertEqual(len(loaded.data["interview_sessions"]), 1)
            self.assertFalse(loaded.data["verification_records"])
            self.assertFalse(loaded.needs_preparation_save)

    def test_discipline_rotates_deterministically(self):
        self.assertEqual(discipline(START), discipline(START))
        self.assertNotEqual(discipline(START), discipline(date(2026, 10, 3)))


if __name__ == "__main__":
    unittest.main()
