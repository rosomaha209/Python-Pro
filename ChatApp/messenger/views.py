from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from messenger.models import Message
from rest_framework import viewsets

from messenger.permissions import IsAuthorOrSuperuser
from rest_framework.decorators import action
from rest_framework.response import Response


@login_required
def chat_view(request):
    # Отримуємо всі повідомлення для чату (можливо, потрібно додаткові фільтри)
    messages = Message.objects.all()
    return render(request, 'chat.html', {'messages': messages})


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthorOrSuperuser]

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        A custom action to get the most recent messages.
        """
        recent_messages = Message.objects.order_by('-date_sent')[:10]
        serializer = self.get_serializer(recent_messages, many=True)
        return Response(serializer.data)