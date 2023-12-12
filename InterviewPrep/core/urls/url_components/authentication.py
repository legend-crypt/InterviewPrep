from django.urls import path
from core.views.authentication import (
    SignInView,
    SignOutView,
    PasswordViewset
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

AUTHENTICATION_URLS = [
     path(
        "api/account/password-reset-request/",
        PasswordViewset.as_view({"post": "password_reset_request"}),
    ),
    path(
        "api/account/password-reset-verify/",
        PasswordViewset.as_view({"post": "verify_password_reset_otp"}),
    ),
    path(
        "api/account/password-reset/",
        PasswordViewset.as_view({"post": "password_reset"}),
    ),
     path(
        "api/account/signin/",
        SignInView.as_view(),
    ),
    path(
        "api/account/signout/",
        SignOutView.as_view({"post": "post"}),
    ),
    path("api/authentication/token/", TokenObtainPairView.as_view()),
    path("api/authentication/token/refresh/", TokenRefreshView.as_view()),
    path("api/authentication/token/verify/", TokenVerifyView.as_view()),
  
]