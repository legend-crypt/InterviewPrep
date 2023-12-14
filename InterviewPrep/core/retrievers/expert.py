from core.models.expert import Expert


def get_experts():
    """Get all experts in the database"""
    experts = Expert.objects.all()
    return experts

def get_expert_by_id(id):
    """get expert by email

    Args:
        id (uuid): uuid field

    Returns:
        Expert: Expert object
    """
    try:
        return Expert.objects.get(expert_id=id)
    except Expert.DoesNotExist:
        return None
    

def get_expert_by_email(email:str) -> Expert:
    """Get Expert by user id

    Args:
        email (str): email field

    Returns:
        Expert: object instance object
    """
    try:
        return Expert.objects.get(user__email=email)
    except Expert.DoesNotExist:
        return None