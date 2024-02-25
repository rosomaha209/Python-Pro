from django.db import models
from django.contrib.auth import get_user_model


class Courses(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(get_user_model(), through='members_app.UserEnrollment')

