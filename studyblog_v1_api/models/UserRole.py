from django.db import models
from studyblog_v1_api.models import UserProfile, Role


class UserRole(models.Model):
    """DB Model for connecting User and their roles"""

    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        null=False
    )

    role = models.ForeignKey(
        to=Role,
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return f"UserId: {self.user_id} | RoleId: {self.role_id}"