from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from studyblog_v1_api.models.UserProfileModel import *
from studyblog_v1_api.serializers import UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    """Handle creating, updating and filtering profiles"""
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = (DB_FIELD_USERNAME,)


class ProfileLoginApiView(ObtainAuthToken):
    """API-Endpoint for receiving authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES