from django.urls import path
from core.views.accounts import AccountViewset

path("acounts/create/", Account.as_view({"post":"create"}), name="")