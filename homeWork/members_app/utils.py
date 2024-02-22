from datetime import date

from django.contrib.auth import get_user_model

from courses_app.models import Courses
from members_app.models import UserEnrollment


# def init_user_course():
#     User = get_user_model()
#
#     user = User.objects.get(id=1)
#
#     course_name = 'Python Pro'
#     course = Courses.objects.get(title=course_name)
#
#     user_enrollment = UserEnrollment(user=user, course=course, date_enrolled=date.today())
#     user_enrollment.save()
#
#
# print(date.today())
