from core.model.accounts import UserAccount
from core.model.profile import Profile

def get_profile_by_id(id) ->Profile:
    """Get profile by id

    Args:
        id (uuid): profile id

    Returns:
        YelloUserProfile: _description_
    """
    try:
        return Profile.objects.get(profile_id=id)
    except Profile.DoesNotExist:
        return None

    
def get_profile_user_email(email) ->Profile:
    """Get profile by user email

    Args:
        email (str): user email

    Returns:
        YelloUserProfile: _description_
    """
    try:
        user = get_user_by_email(email)
        return Profile.objects.get(user.profile)
    except YelloUserProfile.DoesNotExist:
        return None
