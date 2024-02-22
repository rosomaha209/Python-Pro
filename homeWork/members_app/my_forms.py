from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from .models import  UserEnrollment


# class MyForm(forms.Form):
#     username = forms.CharField(label="My username field")
#     email = forms.EmailField(label="Your Email")
#     password = forms.CharField(widget=forms.PasswordInput, validators=password_validators_help_texts())
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     courses = forms.MultipleChoiceField(
#         choices=[('math', 'Math'), ('history', 'History'), ('science', 'Science')],
#         widget=forms.CheckboxSelectMultiple,
#         label='Select your courses'
#     )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = UserEnrollment
        fields = ['course']
