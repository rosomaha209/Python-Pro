from django.contrib.auth import get_user_model
from rest_framework import serializers

from messenger.models import Chat, Message

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ['id', 'author', 'text', 'chat']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        return super().create(validated_data)
