from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from studyblog_v1_api.serializers import UserProfileSerializer
from studyblog_v1_api.utils.request import validate_composite_primary_keys
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.permissions import UserProfilePermission, UserRolePermission, RolePermission
from studyblog_v1_api.db import query, filter
from studyblog_v1_api.services import role_service, user_service
from studyblog_v1_api.models import (
    UserProfileModel,
    UserRoleModel,
    RoleModel,
    DB_FIELD_USERNAME,
    DB_FIELD_ROLE_NAME,
)
from studyblog_v1_api.serializers import (
    UserProfileSerializer,
    UserRoleSerializer,
    RoleSerializer
)


class UserViewSet(ModelViewSet):
    """Handle creating, updating and filtering profiles"""
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    permission_classes = (UserProfilePermission,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_USERNAME,)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            result = user_service.get_item(request, pk)
            return res.success(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"User with the id {pk} does not exist")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
        

    def list(self, request, *args, **kwargs):
        """
           /api/v1/profile/?details=true&user_id=1,2,4
        """
        try:
            result = user_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)


class UserAuthTokenApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RoleViewSet(ModelViewSet):
    """TODO: add description"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()
    permission_classes = (IsAuthenticated, RolePermission)
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_ROLE_NAME,)


class UserRoleViewSet(ModelViewSet):
    """TODO: add description"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserRoleSerializer
    queryset = UserRoleModel.objects.all()
    permission_classes = (IsAuthenticated, UserRolePermission)

    @validate_composite_primary_keys(UserRoleModel, "user", "role")
    def create(self, request, *args, **kwargs):
        """TODO: add description"""
        try:
            result = role_service.create_item(request)
            return res.success(result)
        except IntegrityError as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    @validate_composite_primary_keys(UserRoleModel, "user", "role")
    def update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            result = role_service.update_item(request, pk)
            return res.updated(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"UserRole object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)