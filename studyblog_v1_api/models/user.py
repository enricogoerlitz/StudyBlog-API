from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username, password=None):
        """Create a new user profile"""

        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Create and save a new superuser with given details"""

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfileModel(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    username = models.CharField(max_length=30, unique=True)
    
    # is required of AbstractBaseUser
    is_staff = models.BooleanField(default=False)

    # UserProfileManager -> creating and managing new und current users
    objects = UserProfileManager() 

    USERNAME_FIELD = "username"

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.username
    
    def get_short_name(self):
        return f"{self.username[:5]}..."
    
    def __str__(self):
        """Return string representation of our user for Django-Admin"""
        return self.username




class RoleModel(models.Model):
    """DB Model for storing role names"""

    role_name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        """returns model as string"""
        return self.role_name


class UserRoleModel(models.Model):
    """DB Model for connecting User and their roles"""

    user = models.ForeignKey(
        to=UserProfileModel,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    role = models.ForeignKey(
        to=RoleModel,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    def __str__(self):
        """returns model as string"""
        return f"UserId: {self.user_id} | RoleId: {self.role_id}"