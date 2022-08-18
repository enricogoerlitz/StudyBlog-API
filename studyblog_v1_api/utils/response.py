from rest_framework import status
from rest_framework.response import Response

from typing import Union


def error_500_internal_server_error(exp: Union[Exception, str, dict]) -> Response:
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error_400_bad_request(exp: Union[Exception, str, dict]) -> Response:
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_400_BAD_REQUEST)

def error_401_unauthorized(exp: Union[Exception, str, dict]) -> Response:
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_401_UNAUTHORIZED)

def error_403_forbidden(exp: Union[Exception, str, dict]) -> Response:
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_403_FORBIDDEN)
