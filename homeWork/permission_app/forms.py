from django import forms
from .models import Permission


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'description']
