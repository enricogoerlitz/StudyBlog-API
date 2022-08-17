from rest_framework.serializers import ModelSerializer
from studyblog_v1_api.models.RoleModel import *


class RoleSerializer(ModelSerializer):
    """Serialize Roles"""

    class Meta:
        model = RoleModel
        fields = ("id", DB_FIELD_ROLE_NAME)