""""""
from rest_framework.permissions import BasePermission, SAFE_METHODS


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
            pass
            

        if request.method in ["PUT", "PATCH", "DELETE"]:
            pass

