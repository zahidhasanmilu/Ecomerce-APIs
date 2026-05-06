# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomLoginView,
    PasswordResetRequestView,
    RegisterView,
    ResendVerificationView,
    VerifyEmailByLinkView,
    LogoutView,
    # RequestPasswordResetView,
    # ConfirmPasswordResetView,
    PasswordResetConfirmView,
    UserProfileDetailView,
    ChangePasswordView,
    VerifyEmailView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/verify-email-otp/<uuid:token>/", VerifyEmailView.as_view()),
    path("auth/verify-email-link/<uuid:token>/", VerifyEmailByLinkView.as_view()),
    path(
        'auth/resend-verification/',
        ResendVerificationView.as_view(),
        name='resend_verify',
    ),
    path(
        'password/reset/',
        PasswordResetRequestView.as_view(),
        name='password_reset_request',
    ),
    path(
        'password/reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    # path('auth/token/', CustomLoginView.as_view(), name='token'),
    path('auth/token/', CustomLoginView.as_view(), name='token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('<int:id>/', UserProfileDetailView.as_view(), name='profile-detail'),
]
