from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, request
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from messenger.models import Message


class UserCanEditMessageMixin:
    def dispatch(self, request, *args, **kwargs):
        message_id = kwargs.get('pk')
        message = get_object_or_404(Message, pk=message_id)

        if request.user != message.author:
            return HttpResponseForbidden("Ви не можете редагувати це повідомлення, оскільки не є його автором.")

        if (timezone.now() - message.created_at).days >= 1:
            return HttpResponseForbidden(
                "Ви не можете редагувати це повідомлення, оскільки з моменту його створення пройшло більше суток.")

        return super().dispatch(request, *args, **kwargs)


class UserIsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=kwargs.get('pk'))
        if message.author != request.user:
            return HttpResponseForbidden("Ви не маєте права видаляти це повідомлення, оскільки не є його автором.")
        return super().dispatch(request, *args, **kwargs)


class HasPermissionMixin(UserPassesTestMixin):
    permission_required = 'can_remove_participants'

    def test_func(self):
        return self.request.user.has_perm(self.permission_required)


class AdminOrPermissionRequiredMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        has_permission = self.request.user.has_perm(self.permission_required)
        return self.request.user.is_superuser or has_permission


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser




class ModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Moderators').exists()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class LoggedInRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated


class IPBasedAccessMixin(UserPassesTestMixin):
    allowed_ips = ['127.0.0.1', '192.168.1.1']

    def test_func(self):
        return self.request.META.get('REMOTE_ADDR') in self.allowed_ips


class AjaxRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.is_ajax()


class ReadOnlyModeMixin(UserPassesTestMixin):
    def test_func(self):
        return not settings.READ_ONLY_MODE

    def handle_no_permission(self):
        return HttpResponseForbidden("Sorry, the site is in read-only mode.")


class SubscriptionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_subscription()

    def handle_no_permission(self):
        return HttpResponseForbidden("You need to have a subscription to access this page.")


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active

    def handle_no_permission(self):
        return HttpResponseForbidden("Your account is inactive.")
