from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Chat(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User)

    class Meta:
        permissions = [
            ("can_change_chat", "Can change chat permissions"),
            ("can_create_chat", "Can create chat permissions"),
        ]


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def can_edit(self, user):
        return user == self.author

    def can_delete(self, user):
        if user == self.author:
            if timezone.now() - self.created_at > timezone.timedelta(days=1):
                return False
            else:
                return True
        return False
