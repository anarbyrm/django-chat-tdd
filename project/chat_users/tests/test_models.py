from django.test import TestCase, Client

from chat_users.models import User


class UserModelTests(TestCase):
    def test_user_models_objects_can_be_created_with_email(self):
        email = 'test@example.com'
        user = User.objects.create(email=email, password='test123')
        count = User.objects.count()
        u1 = User.objects.filter(id=1).first()
        self.assertEqual(count, 1)
        self.assertEqual(u1.email, email)