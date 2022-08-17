from django.db import models
from studyblog_v1_api.models import UserProfileModel, RoleModel


DB_FIELD_USER_ID = "user_id"
DB_FIELD_ROLE_ID = "role_id"


class UserRoleModel(models.Model):
    """DB Model for connecting User and their roles"""

    user = models.ForeignKey(
        to=UserProfileModel,
        on_delete=models.CASCADE,
        null=False
    )

    role = models.ForeignKey(
        to=RoleModel,
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return f"UserId: {self.user_id} | RoleId: {self.role_id}"