from core.models.verification_token import VerificationToken, PasswordVerificationToken
from core.retrievers.accounts import *


def get_verification_token(email: str):
    """Get an email verification token 'otp' object if it exists"""
    try:
        token = VerificationToken.objects.get(email=email)
    except VerificationToken.DoesNotExist:
        return None
    else:
        return token


def get_password_verification_token(email: str):
    """Get an email verification token 'otp' object if it exists"""
    try:
        token = PasswordVerificationToken.objects.get(email=email)
    except PasswordVerificationToken.DoesNotExist:
        return None
    else:
        return token
