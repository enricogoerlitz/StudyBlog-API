from rest_framework.serializers import ModelSerializer
from studyblog_v1_api.models import (
    UserProfileModel,
    RoleModel,
    UserRoleModel,
    DB_FIELD_ALL,
    DB_FIELD_USERNAME,
    DB_FIELD_PASSWORD,
)


class UserProfileSerializer(ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = UserProfileModel
        fields = DB_FIELD_ALL
        extra_kwargs = {
            DB_FIELD_PASSWORD: {
                "write_only": True,
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        """Handle creating a new user"""
        return UserProfileModel.objects.create_user(
            username=validated_data.get(DB_FIELD_USERNAME),
            password=validated_data.get(DB_FIELD_PASSWORD),
        )
    
    def update(self, instance, validated_data):
        """Handle updating an user"""
        if DB_FIELD_PASSWORD in validated_data:
            instance.set_password(validated_data.pop(DB_FIELD_PASSWORD))
        
        return super().update(instance, validated_data)


class RoleSerializer(ModelSerializer):
    """Serialize Roles"""

    class Meta:
        model = RoleModel
        fields = DB_FIELD_ALL


class UserRoleSerializer(ModelSerializer):
    """Serialize an UserRoleModel"""

    class Meta:
        model = UserRoleModel
        fields = DB_FIELD_ALL