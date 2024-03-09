from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.http import request, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Chat, Message


class MessageEditDeleteMixin(UserPassesTestMixin):

    def test_func(self):
        message = self.get_object()
        time_limit = timezone.now() - timezone.timedelta(days=1)
        can_edit = message.author == self.request.user and message.created_at > time_limit
        return can_edit

    def handle_no_permission(self):
        return HttpResponse('You do not have permission to edit this message.')


class SuperuserRequiredMixin(AccessMixin):
    """Mixin that allows only superusers to access the view."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):

        return redirect('login')

class ActiveUserMixin(UserPassesTestMixin):
    """
    Переконується, що користувач є активним.
    """

    def test_func(self):
        return self.request.user.is_active


class ChatOwnerMixin(UserPassesTestMixin):
    """
    Переконується, що користувач є власником чату.
    """

    def test_func(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return self.request.user == chat.owner


class EditableMessageMixin(UserPassesTestMixin):
    """
    Перевіряє, чи може користувач редагувати повідомлення.
    """

    def test_func(self):
        message_id = self.kwargs.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        return self.request.user == message.author and \
            (timezone.now() - message.timestamp).days < 1


class DeleteMessageMixin(UserPassesTestMixin):
    """
    Дозволяє користувачеві видаляти власні повідомлення під певними умовами.
    """

    def test_func(self):
        message_id = self.kwargs.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        return self.request.user == message.author


class RecentMessageMixin:
    """
    Фільтрує повідомлення, які були додані не більше дня тому.
    """

    def get_queryset(self):
        return super().get_queryset().filter(timestamp__gte=timezone.now() - timezone.timedelta(days=1))


class ChatParticipantsMixin:
    """
    Додає список учасників чату до контексту.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        context['participants'] = chat.users.all()
        return context


class UserCanViewChatMixin(UserPassesTestMixin):
    """
    Переконується, що користувач є учасником чату.
    """

    def test_func(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return self.request.user in chat.users.all()


class RedirectToLoginMixin:
    """
    Перенаправляє неавторизованих користувачів на сторінку входу.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


