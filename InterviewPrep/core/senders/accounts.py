from core.models.accounts import UserAccount
from core.serializers.accounts import UserAccountSerializer


import pytz


UTC = pytz.UTC

def create_user(email, password):
    """Create user"""
    user = UserAccount.objects.create_user(email=email, password=password)
    return user




def update_user(data, user: UserAccount):
    """Update user profile"""
    serializer = UserAccountSerializer(
        data=data, instance=user, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return None
