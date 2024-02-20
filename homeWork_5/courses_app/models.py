from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    enrolled_users = models.ManyToManyField('auth.User', through='members_app.UserEnrollment')  # Використовуємо зворотнє посилання

    def __str__(self):
        return self.title
