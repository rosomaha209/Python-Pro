from django.urls import path
from messenger.views import (
    CreateChatView,
    ChatDetailView,
    AddUserToChatView,
    RemoveUserFromChatView,
    EditMessageView,
    DeleteMessageView,
)

urlpatterns = [
    path('create_chat/', CreateChatView.as_view(), name='create_chat'),
    path('chat_detail/<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('add_user_to_chat/<int:chat_id>/<int:user_id>/', AddUserToChatView.as_view(), name='add_user_to_chat'),
    path('remove_user_from_chat/<int:chat_id>/<int:user_id>/', RemoveUserFromChatView.as_view(), name='remove_user_from_chat'),
    path('edit_message/<int:message_id>/', EditMessageView.as_view(), name='edit_message'),
    path('delete_message/<int:message_id>/', DeleteMessageView.as_view(), name='delete_message'),
]
