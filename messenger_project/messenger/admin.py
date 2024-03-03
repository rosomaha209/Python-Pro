from django.contrib import admin

from messenger.models import Message, Chat

admin.site.register(Message)
admin.site.register(Chat)