from django.urls import path
from .views import grant_permission, permission_list

urlpatterns = [
    path('grant-permission/', grant_permission, name='permission_app'),
    path('permission-list/', permission_list, name='permission_list'),
]
