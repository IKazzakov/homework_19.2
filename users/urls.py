
from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, SuccessVerifyView, ErrorVerifyView, \
    VerifyEmail

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/<token>/', VerifyEmail.as_view(), name='verify_email'),
    path('success_verify/', SuccessVerifyView.as_view(), name='success_verify'),
    path('error_verify/', ErrorVerifyView.as_view(), name='error_verify'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
]
