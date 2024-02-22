from django.urls import path
from .views import UserInputView, UserOutputView, UserSessionView, EnrollmentCreateView, EnrollmentDeleteView, \
    EnrollmentListView

urlpatterns = [
    path('input/', UserInputView.as_view(), name='user_input'),
    path('output/', UserOutputView.as_view(), name='user_output'),
    path('session/', UserSessionView.as_view(), name='user_session'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/delete/<int:enrollment_id>/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]