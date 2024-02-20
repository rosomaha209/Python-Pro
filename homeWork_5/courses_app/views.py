import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from .form import EnrollCourseForm
from .models import Course
from members_app.models import UserEnrollment

from members_app.my_forms import MemberForm

from members_app.models import Member


@login_required
def courses_page(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        # ���� ���������� ����������������, ������������ ������� � ������������ �� ���� �������
        return render(request, 'courses_app/courses.html', {'message': 'This is the Courses page', 'courses': courses})
    else:

        # ���� ���������� �� ����������������, ������������ ������� � ������������ ��� ��������� �������
        return render(request, 'courses_app/courses.html', {'message': 'You have no permissions to view this page'})
        # �������� ����� ��������� �� ������� �����


# @login_required
# def enroll_course(request):
#     if request.method == 'POST':
#         form = EnrollCourseForm(request.POST)
#         if form.is_valid():
#             # ���������� ��� �����, �� ��� �������
#             # ���������, ����� �������� ��������� ����������� �� ����
#             selected_user = form.cleaned_data['users']
#             selected_course = form.cleaned_data['courses']
#             # ������� ���� ����� ������� ���
#             return redirect('dashboard')  # ��������������� �� ���� ������� ���� ������ �������
#     else:
#         form = EnrollCourseForm()
#
#     return render(request, 'enroll_course.html', {'form': form})
#

class CreateCourseView(CreateView):
    model = Course
    fields = ['title']
    success_url = '/'

    def form_valid(self, form):
        # ���������� �����
        response = super().form_valid(form)

        # ��������� ��'���� ����������� � ����� � �����
        user = self.request.user
        course = form.instance

        # ��������� ����������� �� �����
        user_enrollment = UserEnrollment.objects.create(user=user, course=course)
        user_enrollment.save()

        return super().form_valid(form)


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses_app/enroll_course.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_form'] = EnrollCourseForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            course = form.cleaned_data['courses']
            user = request.user
            try:
                member = Member.objects.get(user=user)
            except Member.DoesNotExist:
                member = Member.objects.create(user=user)
            # ����������, �� ���������� �� �� ��������� �� ��� ����
            if course not in member.courses.all():
                member.courses.add(course)
            # ��������� ��� ��� �����������
            member.save()
            return redirect('output_page')
        else:
            return self.form_invalid(form)