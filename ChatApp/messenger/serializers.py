from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    A serializer for the Message model.
    """

    class Meta:
        model = Message
        fields = ['id', 'content', 'date_sent', 'author']
