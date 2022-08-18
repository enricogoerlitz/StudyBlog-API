from rest_framework.serializers import ModelSerializer

from studyblog_v1_api.models.UserRoleModel import *
#from studyblog_v1_api.utils.errors import ModelValidationError


class UserRoleSerializer(ModelSerializer):
    """Serialize an UserRoleModel"""

    class Meta:
        model = UserRoleModel
        fields = ("id", DB_FIELD_ROLE_ID, DB_FIELD_USER_ID)
        
    

    # def create(self, validated_data):
    #     valid_role_id = validated_data[DB_FIELD_ROLE_ID]
    #     valid_user_id = validated_data[DB_FIELD_USER_ID]
    #     try:
    #         UserRoleModel.objects.get(role_id=valid_role_id, user_id=valid_user_id)
    #         raise ModelValidationError(f"This user still got this role (RoleId: {valid_role_id}, UserId: {valid_user_id}")
    #     except ModelValidationError as exp:
    #         raise exp
    #     except Exception:
    #         return UserRoleModel