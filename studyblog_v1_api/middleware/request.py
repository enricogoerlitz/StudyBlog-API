# mypy: ignore-errors
"""
Module for request middleware as decorators.
"""

from typing import Any, Callable, Union

from django.db.models import Model

from rest_framework.request import Request

from studyblog_v1_api.services import user_service
from studyblog_v1_api.utils import response as res


# HTTP-Methods

GET = "GET"
POST = "POST"
PUT = "PUT"
PATCH = "PATCH"
DELETE = "DELETE"


# Middleware decorators

def isin_role(auth_roles: Union[str, list[str], tuple[str]], auth_way: str = "or") -> Any: 
    """
    Checks, whether the user is in the passed role. 
    It returns an 401-unauthorized Response, of the user is not in the given roles.
    Otherwise (if the user is in role) the view will be executed normally. 
    """

    def decorator(func: Callable[[Any, Request], Any]) -> Any:
        def wrapper(view: Any, request: Request, *args, **kwargs) -> Any:
            isin_result = user_service.isin_role(auth_roles, request, auth_way=auth_way)

            access_denied_response = res.error_401_unauthorized(
                {"error": "Access denied. User hasn't the needed permission to access this resource."}
            )
            access_granted_response = lambda: func(view, request, *args, **kwargs)

            return access_granted_response() if isin_result else access_denied_response
        return wrapper
    return decorator


def is_authenticated(func: Callable[[Any, Request], Any]) -> Any:
    """
    Checks, whether the user is authenticated. 
    It returns an 401-unauthorized Response, of the user is not authenticated.
    Otherwise (if the user is authenticated) the view will be executed normally. 
    """
    def wrapper(view: Any, request: Request, *args, **kwargs) -> Any:
        if request.user.is_authenticated: return func(view, request, *args, **kwargs)
        return res.error_401_unauthorized({"detail": "Authentication credentials were not provided."})
    return wrapper 


def validate_composite_primary_keys(db_model: Model, *keys) -> Any:
    """TODO: add description"""
    def decorator(func: Callable[[Any, Request], Any]) -> Any:
        def wrapper(view: Any, request: Request, *args, **kwargs) -> Any:
            db_key_value_map = {}
            for key in request.data:
                value = request.data[key]
                if key in keys and value: db_key_value_map[key] = value

            if len(db_key_value_map) != len(keys):
                missing_required_fields = [missing_key for missing_key in keys if not missing_key in db_key_value_map]
                return res.error_400_bad_request({"error": {"required fields": missing_required_fields}})
            
            if db_model.objects.filter(**db_key_value_map).exists():
                return res.error_400_bad_request({"error": "Duplicate Key Error. This Object is still existing."})
            
            return func(view, request, *args, **kwargs)
        return wrapper
    return decorator