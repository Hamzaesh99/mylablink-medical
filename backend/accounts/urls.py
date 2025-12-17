from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, ConfirmRegistrationView, UserViewSet, MeView, 
    VerifyEmailView, ResendVerificationView,
    PasswordResetRequestView, PasswordResetConfirmView,
    ChangePasswordView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
	path('', include(router.urls)),
	path('register/', RegisterView.as_view(), name='register'),
	path('confirm-registration/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
	path('me/', MeView.as_view(), name='me'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    
    # Password reset endpoints
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

