from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpRequest
from core.models.verification_token import PasswordVerificationToken
from core.models.accounts import UserAccount
from datetime import datetime, timedelta
import pytz
UTC = pytz.UTC

import random, string
def generate_token(otp_length):
    """Generate token"""
    return ''.join([random.choice(string.ascii_uppercase + string.digits)] for _ in range(otp_length))

def generate_otp(otp_length):
    """
    Generate a one time pin with specified length
    """

    return "".join([random.choice(string.digits) for i in range(otp_length)])


def get_user_from_jwttoken(request: HttpRequest) -> UserAccount:
    "Return a user object when a valid jwt token is set in the request header"
    jwt = JWTAuthentication()
    user = jwt.get_user(
        jwt.get_validated_token((jwt.get_raw_token(jwt.get_header(request))))
    )
    return user

def delete_otp(email):
    """
    Delete otp based on the time
    """

    otp_detail = PasswordVerificationToken.objects.get(email=email)
    if UTC.localize(datetime.now()) > otp_detail.time_generated + timedelta(minutes=30):
        otp_detail.delete()
    else:
        return otp_detail