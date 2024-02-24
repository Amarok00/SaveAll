from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Chat, Message


class ChatModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1, self.user2)

    def test_string_representation(self):
        self.assertEqual(str(self.chat), f"Chat between {self.user1} and {self.user2}")

    def test_get_last_message(self):
        message = Message.objects.create(
            chat=self.chat, author=self.user1, content="Hello"
        )
        self.assertEqual(self.chat.get_last_message(), message)

    def test_unread_messages_count(self):
        # Create a message and mark it as unread
        Message.objects.create(
            chat=self.chat, author=self.user1, content="Hi", is_read=False
        )
        self.assertEqual(self.chat.unread_messages_count(), 1)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1, self.user2)

    def test_string_representation(self):
        message = Message.objects.create(
            chat=self.chat, author=self.user1, content="Hello"
        )
        self.assertEqual(str(message), "Hello")

    def test_save_method_updates_last_message_at(self):
        initial_last_message_at = self.chat.last_message_at
        message = Message.objects.create(
            chat=self.chat, author=self.user1, content="Hi"
        )
        self.assertNotEqual(initial_last_message_at, self.chat.last_message_at)

    def test_sent_at_property(self):
        # Create a message 2 days ago
        message = Message.objects.create(
            chat=self.chat, author=self.user1, content="Hello"
        )
        message.created_at = timezone.now() - timezone.timedelta(days=2)
        message.save()

        self.assertEqual(message.sent_at, "2 days ago")

