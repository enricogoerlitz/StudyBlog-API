""""""

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from studyblog_v1_api.serializers import UserProfileSerializer
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.db import query
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
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_USERNAME,)

    def list(self, request, *args, **kwargs):
        """
           /api/v1/profile/?details=true&user_id=1,2,4
        """

        result = []
        user_data = query.execute(query.base_user_details_query_2)
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

        return Response(result)

        details = request.query_params.get("details")
        user_ids = request.query_params.get("user_id")
        if user_ids:
            user_ids = user_ids.split(",")

        if details and details.lower() == "true":
            # error handling -> bei failing id finding!!!
            # + username!
            return Response(query.execute(query.fetch_all_user_details(user_id=user_ids)))

        if user_ids:
            users = UserProfileModel.objects.filter(id__in=user_ids)
            users = UserProfileSerializer(users, many=True).data
            if len(users) == 0:
                return res.error_400_bad_request(f"No user with the ids {user_ids} found!")
            return Response(users)
        
        # + username!

        return super().list(request, *args, **kwargs)

class UserAuthTokenApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RoleViewSet(ModelViewSet):
    """TODO: add description"""
    #authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()
    # permission_classes = (
    #     permissions.UpdateOwnFeedItem,
    #     IsAuthenticated
    # )
    # filter_backends = (SearchFilter,)
    # search_fields = (DB_FIELD_ROLE_NAME,)


class UserRoleViewSet(ModelViewSet):
    """TODO: add description"""
    #authentication_classes = (TokenAuthentication, )
    serializer_class = UserRoleSerializer
    queryset = UserRoleModel.objects.all()
    # permission_classes = (
    #     permissions.UpdateOwnFeedItem,
    #     IsAuthenticated
    # )

    def create(self, request, *args, **kwargs):
        """TODO: add description"""
        try:
            # service!
            user_id = request.data.get(DB_FIELD_USER_ID)
            role_id = request.data.get(DB_FIELD_ROLE_ID)

            if not user_id or not role_id:
                if user_id is None and not role_id is None:
                    return res.error_400_bad_request("The UserId was null. Please enter an UserId")
                
                if role_id is None and not user_id is None:
                    return res.error_400_bad_request("The RoleId was null. Please enter an RoleId")
                
                return res.error_400_bad_request("The UserId and the RoleId was null. Please enter an UserId as well as an RoleId")

            is_existing = UserRoleModel.objects.filter(user_id=user_id, role_id=role_id).exists()
            if is_existing:
                error_msg = f"Duplicate Key Error. The User with the id {user_id} already has the Role with the id {role_id}"
                return res.error_400_bad_request(error_msg)

            new_user_role = UserRoleModel.objects.create(user_id=user_id, role_id=role_id)
            new_user_role.save()
            return Response(UserRoleSerializer(new_user_role).data) # serialize in fn
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            # service!
            user_id = request.data.get(DB_FIELD_USER_ID)
            role_id = request.data.get(DB_FIELD_ROLE_ID)
            
            curr_user_role = UserRoleModel.objects.filter(id=pk)
            if curr_user_role.count() == 0:
                return res.error_400_bad_request(f"No UserRole with the id {pk} existing!")

            if not user_id or not role_id:
                if user_id is None and not role_id is None:
                    return res.error_400_bad_request("The UserId was null. Please enter an UserId")
                
                if role_id is None and not user_id is None:
                    return res.error_400_bad_request("The RoleId was null. Please enter an RoleId")
                
                return res.error_400_bad_request("The UserId and the RoleId was null. Please enter an UserId as well as an RoleId")

            is_existing = UserRoleModel.objects.filter(user_id=user_id, role_id=role_id).exists()
            if is_existing:
                error_msg = f"Duplicate Key Error. The User with the id {user_id} already has the Role with the id {role_id}"
                return res.error_400_bad_request(error_msg)

            curr_user_role.update(user_id=user_id, role_id=role_id)
            return Response(curr_user_role.values()[0])
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def partial_update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            # service!
            user_id = request.data.get(DB_FIELD_USER_ID)
            role_id = request.data.get(DB_FIELD_ROLE_ID)
            
            curr_user_role = UserRoleModel.objects.filter(id=pk)
            if curr_user_role.count() == 0:
                return res.error_400_bad_request(f"No UserRole with the id {pk} existing!")

            if not user_id and not role_id:
                return res.error_400_bad_request("The UserId and the RoleId was null. Please enter an UserId or an RoleId to update to update this UserRole.")

            if not user_id:
                user_id = curr_user_role.values()[0][DB_FIELD_USER_ID]

            if not role_id:
                role_id = curr_user_role.values()[0][DB_FIELD_ROLE_ID]
            
            is_existing = UserRoleModel.objects.filter(user_id=user_id, role_id=role_id).exists()
            if is_existing:
                error_msg = f"Duplicate Key Error. The User with the id {user_id} already has the Role with the id {role_id}"
                return res.error_400_bad_request(error_msg)

            curr_user_role.update(user_id=user_id, role_id=role_id)
            return Response(curr_user_role.values()[0])
        except Exception as exp:
            return res.error_500_internal_server_error(exp)