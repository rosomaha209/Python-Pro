from django import forms
from django.contrib.auth.models import User, Permission

from .models import Chat, Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'participants']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class UserPermissionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    can_remove_participants = forms.BooleanField(required=False)

    def save_permissions(self):
        selected_user = self.cleaned_data['user']
        permission_codename = 'can_remove_participants'
        permission = Permission.objects.get(codename=permission_codename, content_type__app_label='messenger')

        if self.cleaned_data['can_remove_participants']:
            selected_user.user_permissions.add(permission)
        else:
            selected_user.user_permissions.remove(permission)