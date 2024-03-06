from rest_framework import permissions
from .models import Message


class IsAuthorOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow the author of a message or a superuser to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the message or a superuser
        return obj.author == request.user or request.user.is_superuser
