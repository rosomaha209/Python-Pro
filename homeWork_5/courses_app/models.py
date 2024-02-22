from django.db import models
from django.contrib.auth.models import User


class Courses(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='members_app.UserEnrollment')

    def __str__(self):
        return self.title


