"""TODO: add description"""

from rest_framework.serializers import ModelSerializer

from studyblog_v1_api.utils import type_check
from studyblog_v1_api.db import roles
from studyblog_v1_api.services import user_service
from studyblog_v1_api.models import (
    UserProfileModel,
    RoleModel,
    UserRoleModel,
    DB_FIELD_ALL,
    DB_FIELD_ID,
    DB_FIELD_USERNAME,
    DB_FIELD_PASSWORD,
)


class UserProfileSerializer(ModelSerializer):
    """Serializes a UserProfileModel"""

    class Meta:
        model = UserProfileModel
        fields = (DB_FIELD_ID, DB_FIELD_USERNAME, DB_FIELD_PASSWORD)
        extra_kwargs = {
            DB_FIELD_PASSWORD: {
                "write_only": True,
                "style": {"input_type": "password"},
            }
        }
    
    def update(self, instance, validated_data):
        """Handle updating an user"""
        if DB_FIELD_PASSWORD in validated_data:
            instance.set_password(validated_data.pop(DB_FIELD_PASSWORD))
        
        return super().update(instance, validated_data)


class RoleSerializer(ModelSerializer):
    """Serialize RoleModel"""

    class Meta:
        model = RoleModel
        fields = DB_FIELD_ALL


class UserRoleSerializer(ModelSerializer):
    """Serialize an UserRoleModel"""

    class Meta:
        model = UserRoleModel
        fields = DB_FIELD_ALL