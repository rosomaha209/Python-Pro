from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, FormView

from .my_forms import UserForm, EnrollmentForm
from .models import UserEnrollment
from django.contrib.auth import authenticate, login


class UserInputView(FormView):
    form_class = UserForm
    template_name = 'members_app/user_input.html'
    success_url = '/members/output/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserOutputView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = 'members_app/user_output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UserSessionView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = 'members_app/user_session.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        enrollments = UserEnrollment.objects.filter(user=self.request.user)
        context['enrollments'] = enrollments
        return context


class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = UserEnrollment
    form_class = EnrollmentForm
    template_name = 'members_app/enrollment_form.html'
    success_url = '/members/session/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.enrollment_date = date.today()
        return super().form_valid(form)


class EnrollmentListView(View):
    def get(self, request, *args, **kwargs):
        enrollments = UserEnrollment.objects.filter(user=request.user)
        return render(request, 'members_app/enrollment_list.html', {'enrollments': enrollments})

class EnrollmentDeleteView(View):
    def post(self, request, *args, **kwargs):
        enrollment_id = self.kwargs.get('enrollment_id')
        enrollment = UserEnrollment.objects.get(pk=enrollment_id)
        if enrollment.user == request.user:
            enrollment.delete()
        return redirect('enrollment_list')  # Перенаправлення на список енролментів після видаленняedirect('members_app:user_session')