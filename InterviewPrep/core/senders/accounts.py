from core.models import UserAccount
from django.contrib.auth import get_user_model
import random, string
from core.serializers import CleaningServiceSerializer

import pytz
from datetime import datetime, timedelta

UTC = pytz.UTC

def create_user(email, password):
    """Create user"""
    user = UserAccount.objects.create_user(email=email, password=password)
    return user


def generate_token(otp_length):
    """Generate token"""
    return ''.join([random.choice(string.ascii_uppercase + string.digits)] for _ in range(otp_length))
