"""Handles user routes like role, userrole, and user details"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response

from studyblog_v1_api.serializers import RoleSerializer
from studyblog_v1_api.serializers.UserRoleSerializer import UserRoleSerializer
from studyblog_v1_api.models.RoleModel import RoleModel
from studyblog_v1_api.models.UserRoleModel import UserRoleModel, DB_FIELD_ROLE_ID, DB_FIELD_USER_ID
from studyblog_v1_api.utils import response as res


class RoleViewSet(ModelViewSet):
    """TODO: add description"""
    #authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()
    # permission_classes = (
    #     permissions.UpdateOwnFeedItem,
    #     IsAuthenticated
    # )


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


class UserDetails(APIView):
    """TODO: add description"""

    def get(self, request, *args, **kwargs):
        pass

    # service
    def handle_pk_user_request(self, request):
        pass

    def handle_list_user_request(self, request):
        pass

    def handle_list_filtered_request(self, request):
        pass