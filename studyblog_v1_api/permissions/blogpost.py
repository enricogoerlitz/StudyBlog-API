""""""

from rest_framework.permissions import BasePermission, SAFE_METHODS

from studyblog_v1_api.db import roles
from studyblog_v1_api.services import user_service


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

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.is_authenticated

        if request.method == "POST":
            return user_service.isin_role((roles.STUDENT, roles.ADMIN), request=request)

        if request.method in ["PUT", "PATCH", "DELETE"]:
            if user_service.isin_role(roles.ADMIN, request=request):
                return True
            return obj.user.id == request.user.id
                

