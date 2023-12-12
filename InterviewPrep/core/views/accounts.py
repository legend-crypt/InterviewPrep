from core.models import VerificationToken,PasswordVerificationToken
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.senders.accounts import create_user
from core.retrievers.accounts import *
import threading
from core.utils.emails import email_verification, verification_confirmation_email
from datetime import datetime, timedelta
from core.retrievers.verification_token import get_verification_token
import pytz
UTC = pytz.UTC


class AccountViewset(viewsets.ViewSet):
    """Accounts viewset"""
    def list(self, request):
        """List all the users in the database"""
        context = get_all_users()
        return Response(context, status=status.HTTP_200_OK)

    def create_account(self, request):
        """Create an account for a  user"""
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            context = {"detail": "Missing required registration credentials"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_by_email(email=email)

        if user:
            context = {"detail": "Account with email already exists"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)

        user = create_user(email=email, password=password)

        email_thread = threading.Thread(target=email_verification, args=[email, 6])
        email_thread.start()

        context = {
            "detail": "Account successfully created",
            "user": get_user_information(user),
        }

        return Response(context, status=status.HTTP_201_CREATED)
    

    def send_verification_email(self, request):
        """
        Resends a verification pin to the email used in account creation
        """
        email = request.data.get("email")
        user = get_user_by_email(email)
        if not user:
            context = {"detail": "No account associated with email"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if user.verified:
            return Response(
                {"detail": "Your account has already been verified"},
                status=status.HTTP_208_ALREADY_REPORTED,
            )
        user_token = get_verification_token(email)
        if user_token:
            user_token.delete()
        if email_verification(email, 6):
            context = {"detail": "Verification code successfully sent", "email": email}
            return Response(context, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not send verification code"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def verify_email(self, request):
        """
        Verify the email address in a horux account if supplied
        verification PIN is valid
        """
        email = request.data.get("email")
        otp = request.data.get("otp")

        account = get_user_by_email(email)
        if not account:
            context = {"detail": "No account associated with this email"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if account.verified:
            context = {"detail": "Your account has already been verified"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)

        otp_detail = VerificationToken.objects.get(email=email)
        if otp == otp_detail.otp:
            if UTC.localize(datetime.now()) < otp_detail.time_generated + timedelta(
                minutes=10
            ):
                account.verified = True
                account.save()
                otp_detail.delete()
                email_thread = threading.Thread(
                    target=verification_confirmation_email, args=[email]
                )

                email_thread.start()
                context = {
                    "detail": "Your email has been verified successfully",
                    "user": get_user_information(account),
                }

                return Response(context, status=status.HTTP_200_OK)

        else:
            otp_detail.delete()
            context = {"detail": "This otp has expired Request a new one"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context = {"detail": "The otp you have provided is invalid"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_user(self, request, user_id):
        user = get_user_by_id(user_id)
        if not user:
            context = {"detail": "User does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        context = {
                "detail": "User found",
                "User": get_user_information(user)
            }
        return Response(context, status=status.HTTP_200_OK)

