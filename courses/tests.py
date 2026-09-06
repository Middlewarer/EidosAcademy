from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APIClient


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
        for path, limit, user in [('/api/token/',10,None),('/api/register/',5,None),('/api/me/password/',5,self.user),('/api/token/refresh/',60,None)]:
            cache.clear()
            for index in range(limit + 1):
                request = APIRequestFactory().post(path, {}, format='json')
                if user: force_authenticate(request, user=user)
                response = resolve(path).func(request)
                self.assertEqual(response.status_code, 429 if index == limit else 400)
