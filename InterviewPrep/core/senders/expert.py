from core.models.profile import *
from core.serializers.expert import *

def create_expert(data):
    """Create an expert object"""
    serializer = ExpertSerialiazer(data=data, many=False)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.errors


def update_expert(data, expert):
    "updates a expert"
    serializer = ExpertSerialiazer(data=data, instance=expert, partial=True, many=False)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return None
    
def get_expert_information(expert):
    serializer = ExpertSerialiazer(expert)
    if serializer.is_valid:
        return serializer.data
    else:
        return serializer.errors