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
        self.user = User.objects.create_user(username='user1', password='test12345')
        self.chat = Chat.objects.create(name="Test Chat")
        self.chat.participants.add(self.user)
        self.url = reverse('chat_detail', args=[self.chat.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/messenger/login/?next={self.url}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='user1', password='test12345')
        response = self.client.get(self.url)
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messenger/chat_detail.html')

    def test_form_in_context(self):
        self.client.login(username='user1', password='test12345')
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], MessageForm)

    def test_post_valid_message_form(self):
        self.client.login(username='user1', password='test12345')
        response = self.client.post(self.url, {'text': 'Hello'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.exists())

    def test_post_invalid_message_form(self):
        self.client.login(username='user1', password='test12345')
        response = self.client.post(self.url, {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.exists())


class MessageCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.chat = Chat.objects.create(name="Test Chat")
        self.chat.participants.add(self.user)
        self.create_message_url = reverse('send_message', kwargs={'chat_id': self.chat.id})
        self.url = self.create_message_url

    def test_create_message_view_success(self):
        response = self.client.post(self.create_message_url, {'text': 'Test message'})
        self.assertRedirects(response, reverse('chat_detail', kwargs={'pk': self.chat.pk}))
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().text, 'Test message')

    def test_create_message_view_no_text(self):
        response = self.client.post(self.create_message_url, {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.filter(text='').exists())

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_message_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.create_message_url}')


class FileListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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

        for file_info in files_with_types:
            if file_info['file'].name.endswith('.mp3'):
                self.assertEqual(file_info['file_type'], 'audio')
                self.assertEqual(file_info['content'], '')
            elif file_info['file'].name.endswith('.mp4'):
                self.assertEqual(file_info['file_type'], 'video')
                self.assertEqual(file_info['content'], '')
            elif file_info['file'].name.endswith(('.png', '.jpg', '.jpeg')):
                self.assertEqual(file_info['file_type'], 'image')
                self.assertEqual(file_info['content'], '')
            elif file_info['file'].name.endswith('.txt'):
                self.assertEqual(file_info['file_type'], 'text')
                self.assertIn('text content', file_info['content'])
