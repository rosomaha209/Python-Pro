from django.http import Http404

from .forms import PermissionForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from custom_user_app.models import CustomUser


def grant_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('permission_list')  # Redirect to the permission list
    else:
        form = PermissionForm()
    return render(request, 'permission_app/grant_permission.html', {'form': form})


def permission_list(request):
    # Отримання всіх пермісій
    permissions = Permission.objects.all()

    # Отримання всіх користувачів
    users = CustomUser.objects.all()

    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        permission_id = request.GET.get('permission_id')
        action = request.GET.get('action')

        if user_id is not None:
            try:
                user = CustomUser.objects.get(id=user_id)

            except CustomUser.DoesNotExist:
                raise Http404("CustomUser does not exist")

            permission = Permission.objects.get(id=permission_id)

            if action == 'add':
                user.user_permissions.add(permission)
            elif action == 'remove':
                user.user_permissions.remove(permission)

            return redirect('permission_list')

    return render(request, 'permission_app/permission_list.html', {'permissions': permissions, 'users': users})
