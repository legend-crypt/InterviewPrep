from django.urls import path
from core.views.accounts import (
    AccountViewset,
)

ACCOUNTS_URLS = [
    path(
        "accounts/",
        AccountViewset.as_view({"get": "list"}),
    ),
    path(
        "accounts/create/",
        AccountViewset.as_view({"post": "create_account"}),
    ),
    path(
        "accounts/resend-code/",
        AccountViewset.as_view({"post": "send_verification_email"}),
    ),
    path(
        "accounts/send-verification-code/",
        AccountViewset.as_view({"post": "send_verification_email"}),
    ),
    path(
        "accounts/verify-email/",
        AccountViewset.as_view({"post": "verify_email"}),
        name="verify",
    ),
    path(
        "accounts/retrieve/<str:user_id>/",
        AccountViewset.as_view({"get": "retrieve_user"}),
    ),
  
]
