from django.urls import path
from core.views.accounts import (
    AccountViewset,
)

ACCOUNTS_URLS = [
    path(
        "api/accounts/",
        AccountViewset.as_view({"get": "list"}),
    ),
    path(
        "api/accounts/create/",
        AccountViewset.as_view({"post": "create_account"}),
    ),
    path(
        "api/account/resend-code/",
        AccountViewset.as_view({"post": "send_verification_email"}),
    ),
    path(
        "api/account/send-verification-email/",
        AccountViewset.as_view({"post": "send_verification_email"}),
    ),
    path(
        "api/account/verify-email/",
        AccountViewset.as_view({"post": "verify_email"}),
        name="verify",
    ),
    path(
        "api/account/retrieve/<str:user_id>/",
        AccountViewset.as_view({"get": "retrieve_user"}),
    ),
  
]
