"""
Module for handling UserProfile, Role and UserRole permissions.
"""

from typing import Any

from django.db.models import Model

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from studyblog_v1_api.db import query, roles
from studyblog_v1_api.services import user_service
from studyblog_v1_api.middleware.request import GET


class UserProfilePermission(BasePermission):
    """
    GET:
        - Only Authenticated User (managed in View -> IsAuthenticated)
    
    POST:
        Admin:
            - can create an user (default student or with passed role)
        All:
            - can create an user (student role)

    PUT/PATCH/DELETE:
        Admin:
            - can update or delete all no admin users
        Student:
            - can only update or delete their only profile

    """

    def has_object_permission(self, request: Request, view: Any, obj: Model) -> Any:
        """Handles GET, PUT, PATCH and DELETE access on a specific object."""
        if request.method == GET:
            return True

        if user_service.isin_role(roles.ADMIN, request=request):
            return not user_service.isin_role(roles.ADMIN, id=obj.id)
        return obj.id == request.user.id
        

class UserRolePermission(BasePermission):
    """
    GET/POST/PUT/PATCH:
        Admin:
            - can GET/POST/PUT/PATCH all users
            - can't remove 'admin' role
        Other:
            - can do nothing on this route
    """

    def has_permission(self, request: Request, view: Any) -> Any:
        """Handles GET and POST access."""
        return False if request.method == GET and not user_service.isin_role(roles.ADMIN, request=request) else True

    def has_object_permission(self, request: Request, view: Any, obj: Model) -> Any:
        """Handles GET, PUT, PATCH and DELETE access on a specific object."""
        if not user_service.isin_role(roles.ADMIN, request=request):
            return False

        if request.method == GET:
            return True
        
        admin_id = query.execute(f"""
            SELECT id FROM studyblog_v1_api_rolemodel WHERE role_name = '{roles.ADMIN}'
        """)[0]["id"]
        return not obj.role_id == admin_id


class RolePermission(BasePermission):
    """
    GET/POST/PUT/PATCH:
        Admin:
            - can GET/POST/PUT/PATCH all roles
            - the roles 'admin', 'student', 'visitor' cant be changed
        Other:
            - can do nothing on this route
    """
    
    def has_permission(self, request: Request, view: Any) -> Any:
        """Handles GET and POST access."""
        return False if request.method == GET and not user_service.isin_role(roles.ADMIN, request=request) else True
    
    def has_object_permission(self, request: Request, view: Any, obj: Model) -> Any:
        """Handles GET, PUT, PATCH and DELETE access on a specific object."""
        if not user_service.isin_role(roles.ADMIN, request=request):
            return False

        if request.method == GET:
            return True
        
        return not obj.role_name in [roles.ADMIN, roles.STUDENT, roles.VISITOR]