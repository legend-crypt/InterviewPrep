from django.contrib import admin
from core.models.accounts import UserAccount
admin.site.site_header = "SuccessBuilder Administration"

# Register your models here.
admin.site.register(UserAccount)