from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, SignUpView, DeleteMessageView, EditMessageView, ChatListView, \
    CreateChatView, EditChatView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.chat_list, name='chat_list'),
    path('', ChatListView.as_view(), name='chat_list'),
    path('chat/create/', CreateChatView.as_view(), name='create_chat'),
    path('chat/<int:pk>/edit/', EditChatView.as_view(), name='edit_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/create/', views.create_chat, name='create_chat'),
    path('chat/<int:chat_id>/add_user/', views.add_user_to_chat, name='add_user_to_chat'),
    path('message/<int:pk>/edit/', EditMessageView.as_view(), name='edit_message'),
    path('message/<int:pk>/delete/', DeleteMessageView.as_view(), name='delete_message'),
    path('chat/<int:chat_id>/send_message/', views.send_message, name='send_message'),
    path('chat/<int:chat_id>/remove_participant/<int:participant_id>/', views.remove_participant, name='remove_participant'),
    path('chat/<int:chat_id>/edit/', views.edit_chat, name='edit_chat'),
]
