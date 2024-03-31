from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chats')

    class Meta:
        permissions = [
            ("can_remove_participants", "Можливість видаляти учасників чату"),
            ("can_create_chat", "можливість створювати чати"),
            ("can_delete_chat", "можливість видаляти чати"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chat_detail', kwargs={'pk': self.pk})


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    to_superuser = models.BooleanField(default=False)

    def __str__(self):
        return f'Message by {self.author.username} on {self.created_at.strftime("%Y-%m-%d %H:%M")}'


class UploadedFile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва файлу')
    file = models.FileField(verbose_name='Файл')


class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {'Online' if self.is_online else 'Offline'}"

    def check_if_user_is_active(self):
        inactivity_timeout = timezone.timedelta(seconds=300)  # 5 хвилин
        if self.last_activity and (timezone.now() - self.last_activity) > inactivity_timeout:
            self.is_online = False
            self.save(update_fields=['is_online'])
            print("Статус користувача: ", self.user.username, " offline")
        else:
            self.is_online = True
            self.save(update_fields=['is_online'])
        return self.is_online
