""""""

from rest_framework.serializers import ModelSerializer

from studyblog_v1_api.services import user_service
from studyblog_v1_api.utils import type_check
from studyblog_v1_api.db import roles
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
    """Serializes a user profile object"""

    class Meta:
        model = UserProfileModel
        fields = (DB_FIELD_ID, DB_FIELD_USERNAME, DB_FIELD_PASSWORD)
        extra_kwargs = {
            DB_FIELD_PASSWORD: {
                "write_only": True,
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data, *args, **kwargs):
        """Handle creating a new user"""
        # alles in user_service!
        #req_roles = 

        request = self._context["request"]
        passed_user_role_ids = request.data.get("role_id") # None?

        # {
        #       "username": "NewUser2",
        #       "password": "test",
        #       "role_id": [3, 5, 6]
        # }


        print(passed_user_role_ids)
        user_roles = []
        
        if (
            passed_user_role_ids and
            user_service.isin_role(roles.ADMIN, request=request)
        ):
            # validate roles!
            if type_check.is_list_or_tuple(passed_user_role_ids):
                user_roles = list(passed_user_role_ids)
            else:
                user_roles.append(passed_user_role_ids)
        else:
            user_roles.append(RoleModel.objects.get(role_name=roles.STUDENT).id)
        

        created_user = UserProfileModel.objects.create_user(
            username=validated_data.get(DB_FIELD_USERNAME),
            password=validated_data.get(DB_FIELD_PASSWORD),
        )

        if created_user:
            for role in user_roles:
                UserRoleModel.objects.create(user_id=created_user.id, role_id=role)
            return {
                "id": created_user.id,
                "username": created_user.username,
                "roles": user_roles
            }
            


        return created_user
    
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