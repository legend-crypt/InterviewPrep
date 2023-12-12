from core.models import CleaningServiceUser, VerificationToken, PasswordToken
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.senders.accounts import create_user, create_verification_token
from core.retrievers.accounts import *
import threading
from core.utils import email_verification, verification_confirmation_email
from datetime import datetime, timedelta
import pytz
UTC = pytz.UTC


class AccountViewset(viewsets.ViewSet):
    """Accounts viewset"""

    def create(self, request):
        """Create user"""
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_user_by_email(email)
        if user:
            context = {
                'detail': 'User already exists'
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        user = create_user(email, password)
        user.save()
        context = {"detail": "User created successfully", "user": get_user_information(user)}
        thread = threading.Thread(target=email_verification, args=[email, 4])
        thread.start()
        return Response(context, status=status.HTTP_201_CREATED)
