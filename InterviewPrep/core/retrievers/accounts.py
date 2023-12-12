from core.models.accounts import UserAccount
from core.serializers.accounts  import UserAccountSerializer


def get_user_information(email):
    """Get user information"""
    user = get_user_by_email(email)
    serializer = UserAccountSerializer(user)
    return serializer.data

def get_user_by_email(email):
    """Get user by email"""
    try:
        return UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return None

def get_user_by_id(user_id):
    """Get user by id"""
    try:
        return UserAccount.objects.get(user_id=user_id)
    except UserAccount.DoesNotExist:
        return None


def get_all_users():
    """Get all users"""
    queryset = UserAccount.objects.all()
    serializer = UserAccountSerializer(queryset, many=True)
    return serializer.data

