from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chats')

    class Meta:
        permissions = [
            ("can_remove_participants", "Can remove participants from chat"),
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

    def __str__(self):
        return f'Message by {self.author.username} on {self.created_at.strftime("%Y-%m-%d %H:%M")}'
