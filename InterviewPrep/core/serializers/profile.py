from rest_framework import serialiazers
from core.models.profile import Profile
class ProfileSerialiazer(serialiazers.ModelSerialiazer):
    
    class Meta:
        model = Profile
        fields = "__all__"