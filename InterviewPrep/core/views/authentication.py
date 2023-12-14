from rest_framework import viewsets, status
from rest_framework.response import Response
import threading
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from core.retrievers.accounts import *
from core.retrievers.verification_token import *
from core.utils.general import *
from core.utils.emails import *
import base64
from django.http import HttpRequest
import pytz
UTC = pytz.UTC

class SignInView(APIView):
    """
    Validate user credentials and generate a tokens for user
    """

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Missing required login credential")

        user = get_user_by_email(email)

        if not user:
            context = {"detail": "User not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password) and user.is_active:
            token = RefreshToken.for_user(user)
            user_data = get_user_information(user)
            context = {
                "detail": "Sign in successful",
                "user": user_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
            response = Response(context, status=status.HTTP_200_OK)
            return response
        else:
            raise AuthenticationFailed("Incorrect login credentials provided")


class SignOutView(viewsets.ViewSet):
    """
    Logout out a user and destroy access token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        # Get the base64-encoded refresh token from the request headers
        encoded_refresh_token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]

        # Decode the base64-encoded token
        decoded_refresh_token = base64.b64decode(encoded_refresh_token).decode("utf-8")

        try:
            # Create a RefreshToken instance
            refresh_token = RefreshToken(decoded_refresh_token)

            # Blacklist the refresh token
            refresh_token.blacklist()

            return Response({"detail": "Refresh token has been blacklisted."})
        except Exception as e:
            return Response(
                {"detail": "Unable to blacklist refresh token."}, status=400
            )


class PasswordViewset(viewsets.ViewSet):
    """
    A class for managing password Reset
    """

    def password_reset_request(self, request):
        """
        Method for requesting password reset Link
        """
        email = request.data.get("email")
        user = get_user_by_email(email=email)

        otp_detail = get_password_verification_token(email)
        if otp_detail:
            otp_detail.delete()

        if not user:
            return Response(
                {"detail": "User doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        email_thread = threading.Thread(target=password_reset_otp, args=[email, 6])
        email_thread.start()

        return Response(
            {"detail": "An otp has been sent to your account"},
            status=status.HTTP_200_OK,
        )

    def verify_password_reset_otp(self, request):
        """
        Verify reset password otp
        """
        email = request.data.get("email")
        otp = request.data.get("otp")

        account = get_user_by_email(email)
        if not account:
            context = {"detail": "No account associated with this email"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        otp_detail = get_password_verification_token(email=email)
        if otp == otp_detail.otp:
            if UTC.localize(datetime.now()) < otp_detail.time_generated + timedelta(
                minutes=10
            ):
                otp_detail.delete()
                context = {
                    "detail": "You can reset your password now",
                    "user": get_user_information(account),
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                otp_detail.delete()
                context = {"detail": "This otp has expired. Request a new one"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {"detail": "Otp is invalid"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def password_reset(self, request):
        """
        Verify token & encoded_pk and then reset the password.
        """

        email = request.data.get("email")
        new_password = request.data.get("new_password")
        try:
            user = get_user_by_email(email)
        except USERMODEL.DoesNotExist:
            return Response(
                {"detail": "No user account found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not new_password:
            return Response(
                {"detail": "No password provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
