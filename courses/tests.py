from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APIClient


class ChangePasswordTests(TestCase):
    def setUp(self):
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
