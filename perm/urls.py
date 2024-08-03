from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from .views import (
    RegisterAPIView,
    SeasonTokenObtainPairView,
    EmailVerificationAPIView,
    ResendEmailVerificationAPIView,
    ChangePasswordAPIView,
    ResetPasswordAPIView,
    SetPasswordAPIView,
    ProfileAPIView,
    ProfileImageUploadAPIView,
    ProfileImageResetAPIView,
)

urlpatterns = [
    path(
        "signup/", RegisterAPIView.as_view(), name="register"
    ),
    path(
        "confirm_email/<str:token>/",
        EmailVerificationAPIView.as_view(),
        name="confirm_email",
    ),
    path(
        "resend_confirm_email/",
        ResendEmailVerificationAPIView.as_view(),
        name="resend_confirm_email",
    ),
    path(
        "change_password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path(
        "reset_password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path(
        "set_password/<str:token>",
        SetPasswordAPIView.as_view(),
        name="set_password",
    ),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/upload-image/", ProfileImageUploadAPIView.as_view(), name="upload_profile_image"),
    path("profile/reset-image/", ProfileImageResetAPIView.as_view(), name="reset_profile_image"),
    # JWT
    path("jwt/token/", SeasonTokenObtainPairView.as_view(), name="get_token"),
    path("jwt/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('jwt/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
