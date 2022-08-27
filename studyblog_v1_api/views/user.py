from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from studyblog_v1_api.serializers import UserProfileSerializer
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.utils.request import is_authenticated, isin_role
from studyblog_v1_api.permissions import UserProfilePermission, UserRolePermission, RolePermission
from studyblog_v1_api.db import query, filter
from studyblog_v1_api.services import role_service, user_service
from studyblog_v1_api.models import (
    UserProfileModel,
    UserRoleModel,
    RoleModel,
    DB_FIELD_USERNAME,
    DB_FIELD_USER_ID,
    DB_FIELD_ROLE_ID,
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

    def list(self, request, *args, **kwargs):
        """
           /api/v1/profile/?details=true&user_id=1,2,4
        """
        res = user_service.get_item_list(request)
        return Response({})
        user_ids = request.query_params.get("user_id")
        if user_ids:
            user_ids = user_ids.split(",")
        return res.success(query.execute(filter.fetch_user_details(user_id=user_ids)))


        result = []
        user_data = query.execute(filter.base_user_details_query_2)
        added_users = dict()
        for row in user_data:
            user_id = row["id"]
            if not user_id in added_users.keys():
                added_users[user_id] = len(result)
                result.append({
                    "id": user_id,
                    "username": row["username"],
                    "is_superuser": row["is_superuser"],
                    "is_staff": row["is_staff"],
                    "roles": [] if not row["role_name"] else [row["role_name"]],
                })
                continue
            
            result[added_users[user_id]]["roles"].append(row["role_name"])

        return res.success(result)

        details = request.query_params.get("details")
        user_ids = request.query_params.get("user_id")
        if user_ids:
            user_ids = user_ids.split(",")

        if details and details.lower() == "true":
            # error handling -> bei failing id finding!!!
            # + username!
            return res.success(query.execute(filter.fetch_user_details(user_id=user_ids)))

        if user_ids:
            users = UserProfileModel.objects.filter(id__in=user_ids)
            users = UserProfileSerializer(users, many=True).data
            if len(users) == 0:
                return res.error_400_bad_request(f"No user with the ids {user_ids} found!")
            return res.success(users)
        
        # + username!

        return super().list(request, *args, **kwargs)

class UserAuthTokenApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RoleViewSet(ModelViewSet):
    """TODO: add description"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()
    permission_classes = (IsAuthenticated, RolePermission)
    # filter_backends = (SearchFilter,)
    # search_fields = (DB_FIELD_ROLE_NAME,)


class UserRoleViewSet(ModelViewSet):
    """TODO: add description"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserRoleSerializer
    queryset = UserRoleModel.objects.all()
    permission_classes = (IsAuthenticated, UserRolePermission)

    def create(self, request, *args, **kwargs):
        """TODO: add description"""
        try:
            result = role_service.create_item(request)
            return res.success(result)
        except IntegrityError as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            result = role_service.update_item(request, pk)
            return res.updated(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"UserRole object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)