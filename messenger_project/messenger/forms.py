from django import forms
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

from .models import Chat, Message, UploadedFile


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

    def __init__(self, *args, **kwargs):
        super(UserPermissionForm, self).__init__(*args, **kwargs)
        app_labels = ['messenger']
        permissions = Permission.objects.filter(content_type__app_label__in=app_labels)

        for perm in permissions:
            self.fields[perm.codename] = forms.BooleanField(required=False, label=perm.name)

    def save_permissions(self):
        selected_user = self.cleaned_data['user']

        from .models import Chat
        chat_content_type = ContentType.objects.get_for_model(Chat)

        permissions = Permission.objects.filter(content_type=chat_content_type)

        for perm in permissions:
            has_perm = self.cleaned_data.get(perm.codename, False)
            if has_perm:
                selected_user.user_permissions.add(perm)
            else:
                selected_user.user_permissions.remove(perm)


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['name', 'file']


class TextFileForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
