from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet)


# URLConf
urlpatterns = [
    path('', include(router.urls)),
]
