from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView, TemplateView

from messenger.models import Chat, Message, User

from messenger.forms import MessageForm, UserPermissionForm

from messenger.mixins import UserCanEditMessageMixin, UserIsAuthorMixin, HasPermissionMixin, \
    AdminOrPermissionRequiredMixin


class ChatCreateView(UserPassesTestMixin, CreateView):
    model = Chat
    fields = ['name', 'participants']
    template_name = 'messenger/create_chat.html'
    success_url = reverse_lazy('chat_list')

    def test_func(self):
        return self.request.user.is_superuser


class ChatListView(ListView):
    model = Chat
    template_name = 'messenger/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class ChatDetailView(DetailView):
    model = Chat
    template_name = 'messenger/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = self.get_object()
            message.save()
            return redirect('chat_detail', pk=message.chat.pk)
        return self.render_to_response(self.get_context_data(form=form))


class MessageUpdateView(UserCanEditMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/edit_message.html'

    def get_success_url(self):
        return self.object.chat.get_absolute_url()


class MessageDeleteView(UserIsAuthorMixin, DeleteView):
    model = Message
    template_name = 'messenger/confirm_delete.html'
    success_url = reverse_lazy(
        'chat_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class ChatAddParticipantView(UserPassesTestMixin, UpdateView):
    model = Chat
    template_name = 'messenger/chat_add_participant.html'
    fields = ['participants']
    success_url = reverse_lazy('chat_list')

    def test_func(self):
        return self.request.user.is_superuser


class ChatRemoveParticipantView(AdminOrPermissionRequiredMixin, View):
    permission_required = 'messenger.can_remove_participants'

    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs.get('chat_id'))
        user_to_remove = get_object_or_404(User, pk=request.POST.get('user_id'))
        chat.participants.remove(user_to_remove)
        return redirect('chat_detail', pk=chat.pk)


class UserPermissionView(UserPassesTestMixin, FormView):
    template_name = 'messenger/user_permissions.html'
    form_class = UserPermissionForm
    success_url = reverse_lazy('user_permissions')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save_permissions()
        return super().form_valid(form)


class MessageCreateView(CreateView):
    model = Message
    fields = ['text']
    template_name = 'messenger/create_message.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.chat_id = self.kwargs['chat_id']
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_permissions'] = self.request.user.get_user_permissions()
        return context


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'
