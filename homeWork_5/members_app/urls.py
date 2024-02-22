from django.urls import path
from .views import UserInputView, UserOutputView, UserSessionView, EnrollmentCreateView

urlpatterns = [
    path('input/', UserInputView.as_view(), name='user_input'),
    path('output/', UserOutputView.as_view(), name='user_output'),
    path('session/', UserSessionView.as_view(), name='user_session'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enrollment_create'),
]