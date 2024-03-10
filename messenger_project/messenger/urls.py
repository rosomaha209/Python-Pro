from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import CustomLoginView, CustomLogoutView, SignUpView, ChatCreateView, ChatListView, MessageCreateView, \
    ChatDetailView, MessageUpdateView, MessageDeleteView, ChatAddParticipantView, ChatRemoveParticipantView, \
    UserPermissionView, ProfileView, ChatDeleteView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create_chat/', login_required(ChatCreateView.as_view()), name='create_chat'),
    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chats/<int:chat_id>/send_message/', login_required(MessageCreateView.as_view()), name='send_message'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('chat/<int:pk>/add_participant/', ChatAddParticipantView.as_view(), name='add_participant'),
    path('chat/<int:chat_id>/remove_participant/', ChatRemoveParticipantView.as_view(), name='remove_participant'),
    path('user_permissions/', UserPermissionView.as_view(), name='user_permissions'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat_delete'),

]
