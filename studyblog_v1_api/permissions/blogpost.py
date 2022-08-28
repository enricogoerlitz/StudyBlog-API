"""
Module for handling BlogPost permissions.
"""

from typing import Any

from django.db.models import Model

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from studyblog_v1_api.db import roles
from studyblog_v1_api.services import user_service
from studyblog_v1_api.middleware.request import GET, POST


class BlogPostPermission(BasePermission):
    """
    GET:
        - Only Authenticated User (managed in View -> IsAuthenticated)

    POST:
        Admin:
            - can create blogposts
        Student:
            - can create blogposts
        Other:
            - access denied

    PUT/PATCH/DELETE:
        Admin:
            - can update and delete every blogpost
        Student:
            - can only update or delete their own blogposts
        Other:
            - access denied
    """

    def has_permission(self, request: Request, view: Any) -> Any:
        """Handles GET and POST access."""
        if request.method == GET:
            return True

        if request.method == POST:
            return user_service.isin_role((roles.STUDENT, roles.ADMIN), request=request)

    def has_object_permission(self, request: Request, view: Any, obj: Model) -> Any:
        """Handles GET, PUT, PATCH and DELETE access on a specific object."""
        if request.method == GET:
            return True

        if user_service.isin_role(roles.ADMIN, request=request):
            return True
        return obj.user.id == request.user.id