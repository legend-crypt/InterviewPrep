import pytz
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.contrib.auth import get_user_model
from typing import List, Tuple, Dict
from core.retrievers.accounts import *
from core.retrievers.verification_token import *
from core.senders.verification_token import *
from core.utils.general import generate_otp


UTC = pytz.UTC

SENDER = "InterviewPrep Incorporation <konadulordkweku@gmail.com>"

def email_verification(email: str, otp_length: int):
    """
    Send email verification code to new user
    """

    subject = "InterviewPrep Email Verification Code"
    pin = generate_otp(otp_length)

    sender = SENDER
    receiver = [email]
    html_content = render_to_string(
        "core/accounts/email_verification.html",
        {"pin": pin, "receiver": email},
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email.attach_alternative(html_content, "text/html")

    if email.send():
        token = get_verification_token(receiver)
        if token:
            update_verification_token(token, pin)
        else:
            create_verification_token(receiver, pin)
        return True
    return False





def password_reset_otp(email, otp_length):
    """
    Send email verification code to new user
    """

    subject = "InterviewPrep Password Reset"
    pin = generate_otp(otp_length)

    sender = SENDER
    receiver = [email]
    html_content = render_to_string(
        "core/accounts/reset_password.html",
        {"pin": pin, "receiver": receiver},
    )
    text_content = strip_tags(html_content)
    email_send = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email_send.attach_alternative(html_content, "text/html")

    if email_send.send():
        try:
            existing_token = PasswordVerificationToken.objects.get(email=email)
        except PasswordVerificationToken.DoesNotExist:
            PasswordVerificationToken.objects.create(
                email=email, otp=pin, time_generated=UTC.localize(datetime.now())
            )
            return True
        existing_token.otp = pin
        existing_token.time_generated = UTC.localize(datetime.now())
        existing_token.save()
        return True
    return False


def verification_confirmation_email(email):
    """
    Confirm email address verification
    """
    subject = "InterviewPrep Email Address Verification Confirmation"

    sender = SENDER
    receiver = [email]

    html_content = render_to_string(
        "core/accounts/email_confirmation.html",
        {"receiver": receiver},
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email.attach_alternative(html_content, "text/html")

    if email.send():
        return True
    return False



