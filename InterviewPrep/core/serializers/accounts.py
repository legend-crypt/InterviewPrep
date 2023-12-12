from rest_framework import serializers
from core.models.accounts import *
import bleach


class BleachSerializer(serializers.ModelSerializer):
    """Serializer that applies bleach.clean to string fields"""

    def to_internal_value(self, data):
        cleaned_data = super().to_internal_value(data)

        for field_name, field_value in cleaned_data.items():
            if isinstance(field_value, str):
                cleaned_data[field_name] = bleach.clean(field_value, strip=True)

        return cleaned_data
    
class UserAccountSerializer(BleachSerializer):
    """Serializer for SuccessBuildersUserAccount"""

    class Meta:
        model = UserAccount
        fields = [
            "user_id",
            "email"
        ]
