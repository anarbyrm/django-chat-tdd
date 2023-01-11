from django.test import TestCase
from django.contrib.auth import get_user_model

from chat.models import Chat, Message

User = get_user_model()


class ChatModelTests(TestCase):
    def test_if_chat_model_object_can_be_created(self):
        chat_instance = Chat.objects.create()
        self.assertEqual(str(chat_instance), str(chat_instance.id))


class MessageModelTests(TestCase):
    def test_if_message_model_object_can_be_created(self):
        user = User.objects.create_user(email='testing2@example.com', password='testing_123')
        message = Message.objects.create(
            user=user,
            body='First message!'
        )
        self.assertEqual(str(message), str(message.id))
