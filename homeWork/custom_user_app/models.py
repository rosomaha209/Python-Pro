from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, help_text='Required. Enter a valid email address.')
