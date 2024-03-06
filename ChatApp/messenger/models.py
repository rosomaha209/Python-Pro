from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
