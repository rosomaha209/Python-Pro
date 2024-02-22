from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
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
        context['enrollments'] = enrollments if enrollments.exists() else None
        return context


class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = UserEnrollment
    form_class = EnrollmentForm
    template_name = 'members_app/enrollment_form.html'
    success_url = '/members/session/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_enrolled = date.today()
        return super().form_valid(form)
