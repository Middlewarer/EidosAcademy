from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import (
    Category,
    Course,
    Feedback,
    Module,
    Topic,
    TopicLesson,
    UserCourseProgress,
    UserTopicProgress,
)


class ChangePasswordTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.user = User.objects.create_user(username='learner', password='Old!Forest72Bird')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.payload = {
            'current_password': 'Old!Forest72Bird',
            'new_password': 'New!Ocean83Cloud',
            'confirm_password': 'New!Ocean83Cloud',
        }

    def test_password_is_changed_and_hashed(self):
        response = self.client.post('/api/me/password/', self.payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.payload['new_password']))
        self.assertFalse(self.user.check_password(self.payload['current_password']))
        self.assertNotEqual(self.user.password, self.payload['new_password'])
        self.assertNotIn('password', response.data)

    def test_invalid_passwords_do_not_change_password(self):
        for changes in [
            {'current_password': 'incorrect'},
            {'confirm_password': 'different'},
            {'new_password': '123', 'confirm_password': '123'},
            {'new_password': 'Old!Forest72Bird', 'confirm_password': 'Old!Forest72Bird'},
            {'current_password': ''},
        ]:
            with self.subTest(changes=changes):
                response = self.client.post('/api/me/password/', {**self.payload, **changes}, format='json')
                self.assertEqual(response.status_code, 400)
                self.user.refresh_from_db()
                self.assertTrue(self.user.check_password(self.payload['current_password']))

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/me/password/', self.payload, format='json')
        self.assertIn(response.status_code, [401, 403])


class AuthFlowTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.user = User.objects.create_user(username='authlearner', password='Old!Forest72Bird')
        self.client = APIClient()

    def tokens(self):
        response = self.client.post('/api/token/', {'username': 'authlearner', 'password': 'Old!Forest72Bird'})
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_rotation_logout_and_expired_access(self):
        from rest_framework_simplejwt.tokens import AccessToken
        from datetime import timedelta
        tokens = self.tokens()
        expired = AccessToken(tokens['access'])
        expired.set_exp(lifetime=timedelta(seconds=-1))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(expired))
        self.assertEqual(self.client.get('/api/me/').status_code, 401)
        self.client.credentials()
        rotated = self.client.post('/api/token/refresh/', {'refresh': tokens['refresh']})
        self.assertEqual(rotated.status_code, 200)
        self.assertNotEqual(rotated.data['refresh'], tokens['refresh'])
        self.assertEqual(self.client.post('/api/token/refresh/', {'refresh': tokens['refresh']}).status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rotated.data['access'])
        self.assertEqual(self.client.get('/api/me/').status_code, 200)
        self.client.credentials()
        self.assertEqual(self.client.post('/api/logout/', {'refresh': rotated.data['refresh']}).status_code, 200)
        self.assertEqual(self.client.post('/api/token/refresh/', {'refresh': rotated.data['refresh']}).status_code, 401)

    def test_password_change_revokes_all_old_tokens(self):
        first, second = self.tokens(), self.tokens()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + first['access'])
        response = self.client.post('/api/me/password/', {
            'current_password': 'Old!Forest72Bird', 'new_password': 'New!Ocean83Cloud',
            'confirm_password': 'New!Ocean83Cloud',
        })
        self.assertEqual(response.status_code, 200)
        for pair in [first, second]:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + pair['access'])
            self.assertEqual(self.client.get('/api/me/').status_code, 401)
            self.client.credentials()
            self.assertEqual(self.client.post('/api/token/refresh/', {'refresh': pair['refresh']}).status_code, 401)
        self.assertEqual(self.client.post('/api/token/', {'username': 'authlearner', 'password': 'New!Ocean83Cloud'}).status_code, 200)

    def test_registration_validation_and_hash(self):
        for password in ['123', 'password', '123456789012']:
            self.assertEqual(self.client.post('/api/register/', {'username':'newlearner','password':password,'password2':password}).status_code, 400)
        self.assertEqual(self.client.post('/api/register/', {'username':'newlearner','password':'New!Ocean83Cloud','password2':'different'}).status_code, 400)
        self.assertEqual(self.client.post('/api/register/', {'username':'newlearner','password':'New!Ocean83Cloud','password2':'New!Ocean83Cloud'}).status_code, 201)
        self.assertTrue(User.objects.get(username='newlearner').check_password('New!Ocean83Cloud'))

    def test_throttle_limits(self):
        from django.core.cache import cache
        from rest_framework.test import force_authenticate, APIRequestFactory
        from django.urls import resolve
        for path, limit, user in [('/api/token/refresh/',60,None)]:
            cache.clear()
            for index in range(limit + 1):
                request = APIRequestFactory().post(path, {}, format='json')
                if user: force_authenticate(request, user=user)
                response = resolve(path).func(request)
                self.assertEqual(response.status_code, 429 if index == limit else 400)


class CourseLearningFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='Strong!Pass42')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        category = Category.objects.create(title='Backend')
        self.course = Course.objects.create(
            category=category,
            title='Django',
            description='Course',
            short_description='Course',
            is_published=True,
        )
        self.module = Module.objects.create(
            course=self.course, title='Start', description='Module', order=0
        )
        self.topic = Topic.objects.create(
            module=self.module, title='Intro', description='Topic', order=0
        )
        self.second_module = Module.objects.create(
            course=self.course, title='Advanced', description='Module', order=5
        )
        self.second_topic = Topic.objects.create(
            module=self.second_module, title='Finish', description='Topic', order=0
        )

        TopicLesson.objects.create(parent_topic=self.topic, content='Первый материал')
        TopicLesson.objects.create(parent_topic=self.second_topic, content='Второй материал')

    def test_public_course_and_all_lesson_materials(self):
        self.client.force_authenticate(user=None)
        detail = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data['course']['category_title'], 'Backend')
        self.client.force_authenticate(self.user)
        extra = TopicLesson.objects.create(parent_topic=self.topic, type='video',
            video_url='https://example.com/lesson.mp4', content='Видео', order=2)
        response = self.client.get(f'/api/modules/{self.module.id}/')
        self.assertEqual(response.data['module']['course_id'], self.course.id)
        lessons = response.data['module']['topics'][0]['lessons']
        self.assertEqual(len(lessons), 2)
        self.assertEqual(lessons[1]['id'], extra.id)
        self.assertEqual(lessons[1]['type'], 'video')
        self.assertEqual(lessons[1]['video_url'], extra.video_url)

    def test_empty_topic_cannot_be_completed(self):
        TopicLesson.objects.filter(parent_topic=self.topic).delete()
        response = self.client.post('/api/progress/complete/', {'topic': self.topic.id})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(UserTopicProgress.objects.filter(user=self.user, topic=self.topic, completed=True).exists())

    def test_assign_is_idempotent_and_course_reports_assignment(self):
        first = self.client.post('/api/assign/', {'course_id': self.course.id}, format='json')
        second = self.client.post('/api/assign/', {'course_id': self.course.id}, format='json')

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(
            UserCourseProgress.objects.filter(user=self.user, course=self.course).count(), 1
        )
        detail = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertTrue(detail.data['is_assigned'])
        self.assertEqual(detail.data['continue_module_id'], self.module.id)

    def test_visit_saves_last_place_without_completing_topic(self):
        response = self.client.post(
            '/api/progress/visit/', {'topic': self.topic.id}, format='json'
        )

        self.assertEqual(response.status_code, 201)
        topic_progress = UserTopicProgress.objects.get(user=self.user, topic=self.topic)
        course_progress = UserCourseProgress.objects.get(user=self.user, course=self.course)
        self.assertFalse(topic_progress.completed)
        self.assertEqual(course_progress.last_topic, self.topic)
        module_detail = self.client.get(f'/api/modules/{self.module.id}/')
        self.assertEqual(module_detail.data['last_topic_id'], self.topic.id)

    def test_unpublished_course_cannot_be_assigned_or_visited(self):
        self.course.is_published = False
        self.course.save(update_fields=['is_published'])

        self.assertEqual(
            self.client.post('/api/assign/', {'course_id': self.course.id}, format='json').status_code,
            404,
        )
        self.assertEqual(
            self.client.post('/api/progress/visit/', {'topic': self.topic.id}, format='json').status_code,
            400,
        )

    def test_topic_module_and_course_statuses(self):
        initial = self.client.get(f'/api/modules/{self.module.id}/')
        self.assertEqual(initial.data['module']['status'], 'not_started')
        self.assertEqual(initial.data['course_progress']['percent'], 0)
        self.assertEqual(initial.data['module']['next_module_id'], self.second_module.id)

        self.client.post('/api/progress/visit/', {'topic': self.topic.id}, format='json')
        started = self.client.get(f'/api/modules/{self.module.id}/')
        self.assertEqual(started.data['module']['status'], 'in_progress')
        self.assertEqual(started.data['module']['topics'][0]['status'], 'in_progress')

        first_complete = self.client.post(
            '/api/progress/complete/', {'topic': self.topic.id}, format='json'
        )
        self.assertEqual(first_complete.status_code, 200)
        self.assertEqual(first_complete.data['course_progress']['completed_topics'], 1)
        self.assertEqual(first_complete.data['course_progress']['percent'], 50)
        self.assertEqual(first_complete.data['course_outline'][0]['status'], 'completed')
        self.assertFalse(UserCourseProgress.objects.get(user=self.user, course=self.course).completed)

        final_complete = self.client.post(
            '/api/progress/complete/', {'topic': self.second_topic.id}, format='json'
        )
        self.assertEqual(final_complete.data['course_progress']['status'], 'completed')
        self.assertEqual(final_complete.data['course_progress']['percent'], 100)
        self.assertTrue(UserCourseProgress.objects.get(user=self.user, course=self.course).completed)

        repeated = self.client.post(
            '/api/progress/complete/', {'topic': self.second_topic.id}, format='json'
        )
        self.assertEqual(repeated.status_code, 200)
        self.assertEqual(
            UserTopicProgress.objects.filter(user=self.user, topic=self.second_topic).count(), 1
        )


class FeedbackTests(TestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.client = APIClient()

    def test_guest_can_submit_and_contact_stays_private(self):
        response = self.client.post(
            '/api/feedback/',
            {
                'kind': 'bug',
                'name': 'Тестировщик',
                'contact': 'tester@example.com',
                'message': 'На странице курса не открывается первый урок.',
                'page_url': 'https://eidosacademy.ru/courses/1',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        feedback = Feedback.objects.get()
        self.assertIsNone(feedback.user)
        self.assertEqual(feedback.contact, 'tester@example.com')
        self.assertTrue(feedback.is_public)
        self.assertNotIn('contact', response.data)
        self.assertEqual(response.data['entry']['message'], feedback.message)

    def test_authenticated_feedback_is_linked_to_user(self):
        user = User.objects.create_user(username='feedback-user', password='Strong!Pass42')
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/feedback/',
            {'kind': 'idea', 'message': 'Добавьте заметки рядом с каждым уроком.'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Feedback.objects.get().user, user)

    def test_public_board_only_exposes_moderated_entries(self):
        Feedback.objects.create(
            kind=Feedback.Kind.REVIEW,
            name='Анна',
            contact='private@example.com',
            message='Курс помог спокойно разобраться с основами.',
            is_public=True,
        )
        Feedback.objects.create(
            kind=Feedback.Kind.BUG,
            message='Это сообщение ещё не прошло модерацию.',
        )

        response = self.client.get('/api/feedback/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['entries']), 1)
        self.assertEqual(response.data['entries'][0]['author'], 'Анна')
        self.assertNotIn('contact', response.data['entries'][0])

    def test_short_message_and_honeypot_are_rejected(self):
        short = self.client.post(
            '/api/feedback/', {'kind': 'review', 'message': 'Мало'}, format='json'
        )
        bot = self.client.post(
            '/api/feedback/',
            {'kind': 'review', 'message': 'Сообщение достаточной длины', 'website': 'spam'},
            format='json',
        )

        self.assertEqual(short.status_code, 400)
        self.assertEqual(bot.status_code, 400)
