from django.test import TestCase

from chat_users.models import User, FriendRequest





class UserModelTests(TestCase):
    def test_user_models_objects_can_be_created_with_email(self):
        email = 'test@example.com'
        user = User.objects.create_user(email=email, password='test123')
        count = User.objects.count()
        u1 = User.objects.first()
        self.assertEqual(count, 1)
        self.assertEqual(u1.email, email)


class FriendRequestModelTests(TestCase):
    def test_if_friend_request_model_can_be_created(self):
        user1 = User.objects.create_user(email='testfriend@example.com', password='testing_123')
        user2 = User.objects.create_user(email='test@example.com', password='testing_123')
        request_instance = FriendRequest(sender=user1, receiver=user2)

        self.assertEqual(str(request_instance), f'{user1}->{user2}')

