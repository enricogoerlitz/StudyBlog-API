""""""

from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db import connection

from studyblog_v1_api.models.UserProfileModel import *
from studyblog_v1_api.models.UserRoleModel import UserRoleModel
from studyblog_v1_api.serializers import UserProfileSerializer
from studyblog_v1_api.serializers.users import UserProfileDetailsSerializer
from studyblog_v1_api.db import query


class UserProfileViewSet(ModelViewSet):
    """Handle creating, updating and filtering profiles"""
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_USERNAME,)


class UserProfileAdminManipulationRoute(ModelViewSet):
    """Handle admin user manipulation
    Admins can create, manipulate and delete none admin users
    """
    serializer_class = UserProfileDetailsSerializer
    queryset = UserProfileModel.objects.all()

    def list(self, request, *args, **kwargs):
        obj_res = query.execute(query.fetch_all_user_details())

        return Response(obj_res)

    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, pk, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProfileLoginApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES