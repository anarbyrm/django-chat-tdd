from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from chat.models import Chat, Message

User = get_user_model()


def chat_detail(chat_id):
    return reverse('chat', args=[chat_id])


class MessagingTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testing@example.com',
            password='testing_123'
        )
        self.client.force_login(user=user)

    def test_if_user_can_see_chat_page(self):
        receiver = User.objects.create_user(
            email='testingother@example.com',
            password='testing_123'
        )
        chat = Chat.objects.create()
        url = chat_detail(chat.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_send_message(self):
        receiver = User.objects.create_user(
            email='testingother@example.com',
            password='testing_123'
        )
        user = User.objects.get(id=int(self.client.session['_auth_user_id']))
        user.friends.add(receiver)
        receiver.friends.add(user)
        chat = Chat.objects.create()
        chat.participants.add(receiver, user)
        url = chat_detail(chat.id)
        earliest_message_count = Message.objects.count()
        response = self.client.post(url, {'body': 'Hello!'})
        self.assertEqual(response.status_code, 302)
        latest_message_count = Message.objects.count()
        self.assertEqual(earliest_message_count+1, latest_message_count)


class UserSearchTest(TestCase):
    def test_if_user_can_be_find_with_exact_email(self):
        email = 'testing@example.com'
        User.objects.create_user(email=email, password='testing_123')
        url = reverse('home')
        response = self.client.get(url, {'user-search': email})
        self.assertEqual(response.status_code, 200)






