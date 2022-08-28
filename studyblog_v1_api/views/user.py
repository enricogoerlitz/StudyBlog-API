# mypy: ignore-errors
"""
API-Endpoints for UserProfile, Role, UserRole models.
"""

import requests

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from studyblog_v1_api.serializers import UserProfileSerializer
from studyblog_v1_api.middleware.request import validate_composite_primary_keys
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.utils.exceptions import UnauthorizedException
from studyblog_v1_api.permissions import UserProfilePermission, UserRolePermission, RolePermission
from studyblog_v1_api.services import role_service, user_service
from studyblog_v1_api.db import filter
from studyblog_v1_api.models import (
    UserProfileModel,
    UserRoleModel,
    RoleModel,
    DB_FIELD_ROLE_NAME,
)
from studyblog_v1_api.serializers import (
    UserProfileSerializer,
    UserRoleSerializer,
    RoleSerializer
)


class UserViewSet(ModelViewSet):
    """Handle UserProfile CRUD-Operations"""
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserProfilePermission,)

    def list(self, request: Request, *args, **kwargs):
        """
        Handle GET requests.
        /api/v1/user/
        /api/v1/user/?details=true&user_id=1,2,4
        """
        try:
            result = user_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def retrieve(self, request: Request, pk: int, *args, **kwargs):
        """
        Handle GET by ID requests.
        /api/v1/user/{id}
        /api/v1/user/{id}/details=true
        """
        try:
            result = user_service.get_item(request, pk)
            return res.success(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"User with the id {pk} does not exist")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def create(self, request: Request, *args, **kwargs):
        """Handle POST requests."""
        serializer_ = self.serializer_class(data=request.data)
        if not serializer_.is_valid():
            return res.error_400_bad_request({"error": serializer_.errors})
        try:
            result = user_service.create_user(request, serializer_.data)
            return res.created(result)
        except UnauthorizedException as exp:
            return res.error_400_bad_request(exp)
        except IntegrityError:
            return res.error_400_bad_request("This username is still existing. Choose another one.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)


class UserMeAPIView(APIView):
    """API-Endpoint for receiving current user."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        """Handle GET requests"""
        try:
            if not filter.is_details(request):
                request.GET._mutable = True
                request.query_params["details"] = "true"

            result = user_service.get_item(request, request.user.id)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)


class UserAuthTokenApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class VisitorAuthTokenApiView(APIView):
    """Handle login as visitor."""

    def get(self, request, *args, **kwargs):
        base_url = request.build_absolute_uri().replace("visitor", "")
        res = requests.post(base_url, {"username": "visitor", "password": "test"})
        token = res.json()
        return Response(token, status=res.status_code)


class RoleViewSet(ModelViewSet):
    """Handle Role CRUD-Operations"""
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_ROLE_NAME,)
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, RolePermission)


class UserRoleViewSet(ModelViewSet):
    """Handle UserRole CRUD-Operations"""
    serializer_class = UserRoleSerializer
    queryset = UserRoleModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, UserRolePermission)

    @validate_composite_primary_keys(UserRoleModel, "user", "role")
    def create(self, request, *args, **kwargs):
        """Handle POST requests."""
        try:
            result = role_service.create_item(request)
            return res.success(result)
        except IntegrityError as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    @validate_composite_primary_keys(UserRoleModel, "user", "role")
    def update(self, request, pk, *args, **kwargs):
        """Handle PUT|PATCH requests."""
        try:
            result = role_service.update_item(request, pk)
            return res.updated(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"UserRole object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)