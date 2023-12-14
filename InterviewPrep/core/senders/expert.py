from core.models.expert import Expert
from core.serializers.expert import ExpertSerializer

def create_expert(data) -> ExpertSerializer:
    """Create Expert

    Args:
        data (dict): data dictionary

    Returns:
        ExpertSerializer: ExpertSerializer object
    """
    serialiazer = ExpertSerializer(data=data)
    if serialiazer.is_valid():
        serialiazer.save()
        return serialiazer.data
    return None


def update_expert(expert:Expert, data:dict) -> ExpertSerializer:
    """Update Expert

    Args:
        expert (Expert): Expert object
        data (dict): data dictionary

    Returns:
        ExpertSerializer: ExpertSerializer object
    """
    serializer = ExpertSerializer(instance=expert, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return None