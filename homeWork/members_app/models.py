from courses_app.models import Courses
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class UserEnrollment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title} on {self.enrollment_date}'
