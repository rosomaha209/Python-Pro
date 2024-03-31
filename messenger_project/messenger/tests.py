import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from messenger.models import Chat, Message, UploadedFile
from messenger.forms import MessageForm


class SimpleTest(TestCase):
    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class ChatDetailViewTests(TestCase):
    def setUp(self):
        # Створення користувача і чату для тестів
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.chat = Chat.objects.create(name="Test Chat")
        self.chat.participants.add(self.user)
        self.url = reverse('chat_detail', kwargs={'pk': self.chat.pk})
        self.client.login(username='testuser', password='12345')

    def test_redirect_if_not_logged_in(self):
        # Вилогінюємось для тесту перенаправлення
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("login")}?next={self.url}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        response = self.client.get(self.url)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], MessageForm)

    def test_post_valid_message_form(self):
        response = self.client.post(self.url, {'text': 'Hello, world!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(text='Hello, world!').exists())

    def test_post_invalid_message_form(self):
        response = self.client.post(self.url, {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.filter(text='').exists())


class MessageCreateViewTests(TestCase):
    def setUp(self):
        # Створення користувача для тестування
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Створення чату для тестування
        self.chat = Chat.objects.create(name="Test Chat")
        self.chat.participants.add(self.user)

        # URL для створення повідомлення
        self.create_message_url = reverse('create_message', kwargs={'chat_id': self.chat.id})

    def test_create_message_view_success(self):
        # Тест на успішне створення повідомлення
        response = self.client.post(self.create_message_url, {'text': 'Test message'})
        self.assertEqual(response.status_code, 302)  # Перевірка на перенаправлення
        self.assertTrue(Message.objects.exists())  # Перевірка чи повідомлення створено

    def test_create_message_view_no_text(self):
        # Тест на відсутність тексту у повідомленні
        response = self.client.post(self.create_message_url, {'text': ''})
        self.assertEqual(response.status_code, 200)  # Форма не повинна бути валідною, тому не перенаправляємо
        self.assertFalse(Message.objects.exists())  # Повідомлення не повинно створюватися

    def test_redirect_after_message_creation(self):
        # Тест на перенаправлення після створення повідомлення
        response = self.client.post(self.create_message_url, {'text': 'Another test message'}, follow=True)
        self.assertRedirects(response,
                             reverse('chat_detail', kwargs={'chat_id': self.chat.id}))  # Перевірка URL перенаправлення


class FileListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Створення тестових файлів
        cls.audio_file = UploadedFile.objects.create(
            name='test_audio',
            file=SimpleUploadedFile('test_audio.mp3', b'audio_content', content_type='audio/mp3')
        )
        cls.video_file = UploadedFile.objects.create(
            name='test_video',
            file=SimpleUploadedFile('test_video.mp4', b'video_content', content_type='video/mp4')
        )
        cls.image_file = UploadedFile.objects.create(
            name='test_image',
            file=SimpleUploadedFile('test_image.jpg', b'image_content', content_type='image/jpeg')
        )
        cls.text_file = UploadedFile.objects.create(
            name='test_text',
            file=SimpleUploadedFile('test_text.txt', b'text content', content_type='text/plain')
        )
        cls.missing_file = UploadedFile.objects.create(
            name='missing_file',
            file=SimpleUploadedFile('missing_file.txt', b'', content_type='text/plain')
        )

        # Створення шляху до неіснуючого файлу
        missing_file_path = os.path.join(settings.MEDIA_ROOT, cls.missing_file.file.name)
        if os.path.exists(missing_file_path):
            os.remove(missing_file_path)

    def test_files_displayed_in_context(self):
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('files_with_types', response.context)
        files_with_types = response.context['files_with_types']
        self.assertEqual(len(files_with_types), 4)  # Перевіряємо, що 4 файли в контексті, а неіснуючий видалено

    def test_file_types_and_content(self):
        response = self.client.get(reverse('file_list'))
        files_with_types = response.context['files_with_types']

        # Перевірка типів файлів і вмісту текстового файлу
        for file_info in files_with_types:
            if file_info['file'].name == 'test_text.txt':
                self.assertEqual(file_info['file_type'], 'text')
                self.assertEqual(file_info['content'], 'text content')
            else:
                self.assertNotEqual(file_info['file_type'], 'text')