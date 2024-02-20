from django import forms
from .models import Course
from django.contrib.auth.models import User


class EnrollCourseForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select)
    courses = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select)


# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['name']