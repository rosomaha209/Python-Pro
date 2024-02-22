from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView

from .form import CourseForm
from .models import Courses


class CourseListView(ListView):
    model = Courses
    template_name = 'courses_app/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Courses
    form_class = CourseForm
    template_name = 'courses_app/course_form.html'
    success_url = '/courses/'
