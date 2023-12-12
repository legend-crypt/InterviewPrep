from django.contrib.auth import get_user_model
from django.http import HttpRequest
from core.serializers import *
from core.retrievers.verification_token import *
import pytz
from datetime import datetime


USERMODEL = get_user_model()
UTC = pytz.UTC


def create_verification_token(email: str, pin: str):
    """Create verification token object"""
    if not get_verification_token(email):
        email_str = email[0] if isinstance(email, list) and len(email) > 0 else ""
        time_generated = UTC.localize(datetime.now())
        VerificationToken.objects.create(
            email=email_str, otp=pin, time_generated=time_generated
        )


def update_verification_token(token_object: VerificationToken, pin: str):
    """Update verfication token object"""
    token_object.otp = pin
    token_object.time_generated = UTC.localize(datetime.now())
    token_object.save()
