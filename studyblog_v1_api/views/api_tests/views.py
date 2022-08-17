from rest_framework.views import APIView
from rest_framework.response import Response

class TestApiView(APIView):
    """Tests the API without any permissions"""

    def get(self, request, format=None):
        return Response({
            "response": "successful", 
            "message": "You successful send a request to this api! Use /v1/api/login to get your token or \
            /v1/api/register to register and get your token."
        })
