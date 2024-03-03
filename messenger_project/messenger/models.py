from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')  # Зв'язок з моделлю Chat

    def __str__(self):
        return f'{self.author.username} - {self.timestamp}'


class Chat(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_chats')

    def __str__(self):
        return self.name
