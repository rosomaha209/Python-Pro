from datetime import date

from django.contrib.auth.models import User
from django.db import models

from courses_app.models import Courses


class UserEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=date.today())  # Забезпечуємо значення за замовчуванням

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title} on {self.enrollment_date}'
