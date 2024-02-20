from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    courses = models.ManyToManyField('courses_app.Course')  # Використовуємо зворотнє посилання

    def __str__(self):
        return self.name


class UserEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses_app.Course', on_delete=models.CASCADE)  # Використовуємо зворотнє посилання
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
