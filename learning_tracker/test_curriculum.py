import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from mastery_curriculum import CURRICULUM, all_task_ids, all_topic_ids
from daily_plan import (
    CAREER_ACTIONS, CAREER_MINUTES, DAILY_QUESTS, MAX_MINUTES, REVIEW_MINUTES, ROADMAP_PHASES,
    START_DATE, VERIFICATION_MINUTES, build_daily_plan,
    TRACK_PRIORITY,
)
from app import Store
from career_readiness import readiness_summary, topic_verified
from progress_insights import calendar_day, completed_topics, interview_prompt, overdue_tasks, weekly_summary


class CurriculumTests(unittest.TestCase):
    def test_curriculum_has_expected_scale(self):
        self.assertEqual(len(CURRICULUM), 10)
        self.assertEqual(len(all_topic_ids()), 240)
        self.assertEqual(len(all_task_ids()), 384)

    def test_every_topic_has_clear_learning_track(self):
        prompts = []
        for track in CURRICULUM:
            self.assertEqual(len(track["topics"]), 24)
            for topic_index, topic in enumerate(track["topics"], 1):
                expected = 2 if track["id"] in {"python", "sql", "django", "testing", "async", "algorithms"} else 1
                self.assertEqual(len(topic["tasks"]), expected)
                self.assertGreater(len(topic["theory"]), 40)
                self.assertTrue(topic["pitfall"])
                self.assertTrue(topic["mastery"])
                self.assertIn(topic["title"], topic["mentor_prompt"])
                self.assertIn("ЭТАП 1 — ПОЛНАЯ ТЕОРИЯ И КОНСПЕКТ", topic["mentor_prompt"])
                self.assertIn("ЭТАП 2 — ПРОВЕРКА ЗНАНИЙ", topic["mentor_prompt"])
                self.assertIn("ЭТАП 3 — ПОВТОРНОЕ ОБУЧЕНИЕ", topic["mentor_prompt"])
                self.assertIn("Не начинай с диагностики", topic["mentor_prompt"])
                self.assertIn("только 3 коротких проверки", topic["mentor_prompt"])
                self.assertIn("Карту урока", topic["mentor_prompt"])
                self.assertIn("КОНТРОЛЬ КАЧЕСТВА", topic["mentor_prompt"])
                self.assertIn("Не повторяй и не перефразируй", topic["mentor_prompt"])
                self.assertIn("strong junior", topic["mentor_prompt"])
                self.assertGreater(len(topic["mentor_prompt"]), 1200)
                prompts.append(topic["mentor_prompt"])
                for task in topic["tasks"]:
                    self.assertIn(task["difficulty"], {"easy", "medium", "hard"})
                    self.assertGreater(task["minutes"], 0)
                    self.assertEqual(task["steps"], [])
                self.assertLessEqual(len(topic["tasks"]), 2)
        self.assertEqual(len(prompts), len(set(prompts)))

    def test_ids_are_unique(self):
        task_ids = all_task_ids()
        topic_ids = all_topic_ids()
        self.assertEqual(len(task_ids), len(set(task_ids)))
        self.assertEqual(len(topic_ids), len(set(topic_ids)))

    def test_every_assignment_is_concrete_and_unique(self):
        tasks = [task for track in CURRICULUM for topic in track["topics"] for task in topic["tasks"]]
        self.assertEqual(len(tasks), 384)
        self.assertEqual(len({task["case"] for task in tasks}), 240)
        for task in tasks:
            self.assertEqual(task["steps"], [])
            self.assertTrue(task["statement"])
            self.assertTrue(task["deliverable"])
            self.assertTrue(task["example"])
            self.assertEqual(task["constraints"], [])
            self.assertEqual(task["checks"], [])
            self.assertGreater(len(task["case"]), 35)

    def test_algorithm_topics_have_one_short_practice_and_final_exam(self):
        track = next(item for item in CURRICULUM if item["id"] == "algorithms")
        for topic_index, topic in enumerate(track["topics"], 1):
            self.assertEqual(len(topic["tasks"]), 2)
            self.assertEqual(topic["tasks"][0]["kind"], "theory")
            code_tasks = [task for task in topic["tasks"] if task["kind"] == "code"]
            self.assertEqual(len(code_tasks), 1)
            for task in code_tasks:
                self.assertTrue(task["external_url"].startswith("https://leetcode.com/problems/"))
                self.assertLessEqual(task["minutes"], 25)
                self.assertIn("Ориентир", task["statement"])
        self.assertIn("exam_prompt", track["topics"][-1]["exam"])
        self.assertIn("Не повторяй и не перефразируй", track["topics"][-1]["exam"]["exam_prompt"])

    def test_topics_do_not_receive_irrelevant_practice(self):
        theory_only = {"http", "git", "linux", "docker"}
        coding = {"python", "sql", "django", "testing", "async"}
        for track in CURRICULUM:
            for topic_index, topic in enumerate(track["topics"], 1):
                kinds = [task["kind"] for task in topic["tasks"]]
                if track["id"] in theory_only:
                    self.assertEqual(kinds, ["theory"])
                elif track["id"] in coding:
                    self.assertEqual(kinds, ["theory", "code"])
                else:
                    self.assertEqual(kinds, ["theory", "code"])
                if track["id"] != "algorithms":
                    self.assertEqual(topic["practice_links"], [])
            self.assertIn("exam", track["topics"][-1])

    def test_start_date_and_existing_progress_are_preserved(self):
        self.assertEqual(START_DATE, date(2026, 10, 2))
        existing_id = CURRICULUM[0]["topics"][0]["tasks"][0]["id"]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "progress.json"
            path.write_text(json.dumps({"learning_model": 6, "completed": [existing_id]}), encoding="utf-8")
            store = Store(path)
            self.assertTrue(store.solved(existing_id))
            self.assertEqual(store.data["daily_target_hours"], 9)
            self.assertFalse(topic_verified(store, CURRICULUM[0]["topics"][0]["id"]))

    def test_daily_plan_is_complete_and_skips_sundays(self):
        plan = build_daily_plan()
        self.assertGreater(len(plan), 50)
        self.assertLess(len(plan), 130)
        self.assertTrue(all(day["topics"] for day in plan))
        self.assertTrue(all(0 <= len(day["task_ids"]) <= 14 for day in plan))
        self.assertTrue(all(REVIEW_MINUTES < day["minutes"] <= MAX_MINUTES for day in plan))
        self.assertTrue(all(day["review_minutes"] == REVIEW_MINUTES for day in plan))
        self.assertTrue(all(day["verification_minutes"] == VERIFICATION_MINUTES for day in plan))
        self.assertTrue(all(day["career_minutes"] == CAREER_MINUTES for day in plan))
        self.assertTrue(all(15 <= day["career_minutes"] <= 30 for day in plan))
        self.assertTrue(all(day["consolidation_minutes"] >= 0 for day in plan))
        average_minutes = sum(day["minutes"] for day in plan) / len(plan)
        self.assertEqual(average_minutes, 540)
        self.assertEqual(len({day["quest"]["key"] for day in plan}), len(plan))
        self.assertTrue(all(day["quest"]["prompt"] for day in plan))
        self.assertTrue(all(day["date"].weekday() != 6 for day in plan))
        planned_topics = [topic["id"] for day in plan for _track, topic in day["topics"]]
        planned_tasks = [task_id for day in plan for task_id in day["task_ids"]]
        self.assertEqual(len(planned_topics), len(set(planned_topics)))
        self.assertEqual(set(planned_topics), set(all_topic_ids()))
        self.assertEqual(len(planned_tasks), len(set(planned_tasks)))
        self.assertEqual(set(planned_tasks), set(all_task_ids()))
        self.assertEqual(plan[0]["topics"][0][0]["id"], "python")
        self.assertNotIn("algorithms", {track["id"] for day in plan[:2] for track, _topic in day["topics"]})
        self.assertTrue(all(action["title"].startswith("HH-разминка") for action in CAREER_ACTIONS))
        career_text = " ".join(action["description"] for action in CAREER_ACTIONS).lower()
        self.assertNotIn("8 подходящих вакансий", career_text)
        self.assertNotIn("5 нанимающих", career_text)
        quest_text = " ".join(
            f'{quest["id"]} {quest["title"]} {quest["description"]} {quest["instruction"]}'
            for quest in DAILY_QUESTS
        ).lower()
        self.assertNotIn("eidosacademy", quest_text)
        self.assertNotIn("project-bridge", quest_text)

    def test_roadmap_prioritizes_job_readiness_and_dependency_order(self):
        plan = build_daily_plan()
        flattened = [(day, track, topic) for day in plan for track, topic in day["topics"]]
        self.assertEqual(set(TRACK_PRIORITY), {track["id"] for track in CURRICULUM})
        for order in TRACK_PRIORITY.values():
            self.assertEqual(sorted(order), list(range(1, 25)))
        self.assertEqual([phase["id"] for phase in ROADMAP_PHASES], [
            "foundation", "backend-start", "working-backend", "production-specialization",
        ])
        for track in CURRICULUM:
            numbers = [topic["number"] for _day, item, topic in flattened if item["id"] == track["id"]]
            self.assertEqual(numbers, TRACK_PRIORITY[track["id"]])

        positions = {topic["id"]: index for index, (_day, _track, topic) in enumerate(flattened)}
        self.assertLess(positions["python-21"], positions["django-01"])
        self.assertLess(positions["django-01"], positions["python-17"])
        self.assertLess(positions["sql-04"], positions["django-01"])
        self.assertLess(positions["http-04"], positions["django-01"])
        self.assertLess(positions["testing-04"], positions["django-01"])
        self.assertLess(positions["django-16"], positions["django-17"])
        self.assertLess(positions["docker-12"], positions["docker-13"])
        first_async = positions["async-01"]
        self.assertTrue(all(index >= first_async for topic_id, index in positions.items() if topic_id.startswith("async-")))
        last_working_django = f'django-{TRACK_PRIORITY["django"][17]:02}'
        self.assertLess(positions[last_working_django], first_async)
        first_algorithm = min(index for topic_id, index in positions.items() if topic_id.startswith("algorithms-"))
        last_python = max(index for topic_id, index in positions.items() if topic_id.startswith("python-"))
        self.assertLess(last_python, first_algorithm)

    def test_no_old_vague_assignment_language_remains(self):
        forbidden = ("production-подобного", "доведи кейс", "реализовать минимальное поведение", "доказать, что ты усвоил")
        for track in CURRICULUM:
            for topic in track["topics"]:
                for task in topic["tasks"]:
                    full_text = " ".join((task["statement"], task["deliverable"], task["acceptance"])).lower()
                    for phrase in forbidden:
                        self.assertNotIn(phrase, full_text)

    def test_pytest_is_isolated_in_testing_track(self):
        for track in CURRICULUM:
            if track["id"] == "testing":
                continue
            for topic in track["topics"]:
                for task in topic["tasks"]:
                    full_text = " ".join((task["deliverable"], task["acceptance"])).lower()
                    self.assertNotIn("pytest", full_text)
                    self.assertNotIn("test_solution.py", full_text)

    def test_today_uses_calendar_day_instead_of_first_incomplete_day(self):
        day, upcoming = calendar_day(date(2026, 10, 3))
        self.assertIsNotNone(day)
        self.assertEqual(day["date"], date(2026, 10, 3))
        self.assertIsNotNone(upcoming)
        self.assertGreater(upcoming["date"], day["date"])

        sunday, next_day = calendar_day(date(2026, 10, 4))
        self.assertIsNone(sunday)
        self.assertEqual(next_day["date"], date(2026, 10, 5))

    def test_weekly_report_and_interview_use_existing_progress(self):
        first_day = build_daily_plan()[0]
        task_id = first_day["task_ids"][0]
        track, topic = first_day["topics"][0]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "progress.json"
            payload = {
                "learning_model": 6,
                "completed": [task["id"] for task in topic["tasks"]],
                "prompt_ready": [topic["id"]],
                "task_records": {
                    task_id: {"attempts": [{"status": "solved", "at": "2026-09-28T12:00"}]}
                },
                "work_seconds": {"2026-09-28": 7200},
                "pomodoro_sessions": {"2026-09-28": 2},
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            store = Store(path)
            store.save_verification(topic["id"], 85, "tests/test_topic.py: verified output with reproducible command", "")
            report = weekly_summary(store, date(2026, 9, 29))
            self.assertEqual(report["focus_seconds"], 7200)
            self.assertEqual(report["sessions"], 2)
            self.assertEqual(report["completed_this_week"], 1)
            self.assertGreaterEqual(report["completed_planned"], 1)
            self.assertFalse(overdue_tasks(store, date(2026, 9, 30)))
            self.assertEqual(overdue_tasks(store, date(2026, 10, 4))[0]["day"]["date"], date(2026, 10, 2))
            ready = completed_topics(store, track)
            self.assertEqual([item["id"] for item in ready], [topic["id"]])
            prompt = interview_prompt(track, ready)
            self.assertIn(topic["title"], prompt)
            self.assertIn("8 вопросов по одному", prompt)
            self.assertIn("не повторяй вопрос", prompt)

    def test_verification_is_separate_from_old_completion(self):
        topic = CURRICULUM[0]["topics"][0]
        with tempfile.TemporaryDirectory() as folder:
            store = Store(Path(folder) / "progress.json")
            store.data["prompt_ready"] = [topic["id"]]
            store.data["completed"] = [task["id"] for task in topic["tasks"]]
            store.save()
            self.assertFalse(topic_verified(store, topic["id"]))
            self.assertEqual(readiness_summary(store)["verified"], 0)
            self.assertGreater(readiness_summary(store)["knowledge"], 0)
            self.assertEqual(completed_topics(store, CURRICULUM[0]), [topic])
            store.save_verification(topic["id"], 85, "tests/test_topic.py: verified output", "")
            self.assertTrue(topic_verified(store, topic["id"]))


if __name__ == "__main__":
    unittest.main()
