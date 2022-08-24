from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from studyblog_v1_api.db import query
from studyblog_v1_api.utils.request import isin_role


class TestAPIView(APIView):
    """Tests the API without any permissions"""
    authentication_classes = (TokenAuthentication,)

    @isin_role(["test25", "test1"], auth_way="or")
    def get(self, request, format=None):

        if request.user.is_authenticated and hasattr(request.user, "password"):
            del request.user.password
            
        return Response({
            "response": "successful", 
            "message": "You successful send a request to this api! Use /v1/api/login to get your token or /v1/api/register to register and get your token.",
            "current_user": str(vars(request.user))
        })
    

class InitApiAPIView(APIView):
    pass
