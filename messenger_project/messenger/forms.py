from django import forms
from .models import Chat, Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
