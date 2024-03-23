from rest_framework import viewsets
from .serializers import ChatSerializer, MessageSerializer
from messenger.models import Message, Chat


class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save()
