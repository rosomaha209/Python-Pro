from datetime import date

from django.contrib.auth.models import User
from django.db import models

from courses_app.models import Courses


class UserEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date_enrolled = models.DateField()

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title} on {self.date_enrolled}'
