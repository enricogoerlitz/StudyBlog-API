from django.db import models


DB_FIELD_ROLE_NAME = "role_name"


class RoleModel(models.Model):
    """DB Model for storing role names"""

    role_name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        """returns model as string"""
        return self.role_name