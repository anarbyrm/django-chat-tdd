from django.test import TestCase, Client
from django.urls import reverse
from django.http import request
from chat_users.models import User


REGISTER_URL = reverse('accounts:register')
LOGIN_URL = reverse('accounts:login')


class PublicUserViewsTests(TestCase):
    def test_if_register_page_can_be_seen(self):
        response = self.client.get(REGISTER_URL)
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_be_registered(self):
        payload = {
            'email': 'test@example.com',
            'password1': 'testing_123',
            'password2': 'testing_123'
        }
        response = self.client.post(REGISTER_URL, data=payload)
        count = User.objects.count()
        user = User.objects.filter(email=payload.get('email'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.exists())
        self.assertEqual(count, 1)
    
    def test_if_bad_request_can_be_handled(self):
        payload_with_weak_pass = {
            'email': 'test@example.com',
            'password1': 'test',
            'password2': 'test'
        }
        response1 = self.client.post(REGISTER_URL, data=payload_with_weak_pass)
        payload_with_bad_email = {
            'email': 'test@example',
            'password1': 'test_123_test',
            'password2': 'test_123_test'
        }
        response2 = self.client.post(REGISTER_URL, data=payload_with_bad_email)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)
    
    def test_if_login_page_can_be_seen(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_login(self):
        user = User.objects.create_user(email='test@example.com', password='testing_123')
        
        payload = dict(
            email='test@example.com',
            password='testing_123'
        )
        response = self.client.post(LOGIN_URL, payload)
        self.assertEqual(response.status_code, 200)


class PrivateUserTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(email='test@example.com', password='testing_123')
        self.client.force_login(user=user)

    def test_if_authenticated_user_can_see_register_and_login_pages(self):
        r1 = self.client.get(REGISTER_URL)
        r2 = self.client.get(LOGIN_URL)
        self.assertNotEqual(r1.status_code, 200)
        self.assertNotEqual(r2.status_code, 200)