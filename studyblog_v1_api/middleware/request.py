"""TODO: add description"""

from rest_framework import status

from studyblog_v1_api.services import user_service
from studyblog_v1_api.utils import response as res


GET = "GET"
POST = "POST"
PUT = "PUT"
PATCH = "PATCH"
DELETE = "DELETE"


class ValidDataWrapper:
    def __init__(self, data, error_msg=None):
        if data is None and error_msg is None:
            raise ValueError("You need to add an error message, if the data is None")

        self.data = data
        self.is_valid = not data is None
        self.errors = error_msg


def get_id_obj(model, Serializer, auto_exe=True):
    """
    Decorator: Checks, whether an id was passed the a get request.

    Args:
        model (DB_Model): an DB Model
        Serializer (Model Serializer): an Model serializer to serialize the model
    """
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            id = request.query_params.get("id")
            if not id: return func(view, *args, **kwargs)

            try:
                obj = model.objects.get(pk=id)
                id_obj = Serializer(obj, many=False).data

                if auto_exe: return Response(id_obj)

                return func(view, request, ValidDataWrapper(id_obj), *args, **kwargs)
            except Exception:
                err_msg = f"Could not find an object with the id {id}"
                if auto_exe:
                    return res.error_400_bad_request({"error": err_msg})

                return func(view, request, ValidDataWrapper(None, err_msg), *args, **kwargs)
        return wrapper
    return decorator

def isin_role(auth_roles, auth_way="or"): 
    """TODO: add description"""

    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            isin_result = user_service.isin_role(auth_roles, request, auth_way=auth_way)

            access_denied_response = res.error_401_unauthorized(
                {"error": "Access denied. User hasn't the needed permission to access this resource."}
            )
            access_granted_response = lambda: func(view, request, *args, **kwargs)

            return access_granted_response() if isin_result else access_denied_response
        return wrapper
    return decorator

def is_authenticated(func):
    """TODO: add description"""
    def wrapper(view, request, *args, **kwargs):
        if request.user.is_authenticated: return func(view, request, *args, **kwargs)
        return res.error_401_unauthorized({"detail": "Authentication credentials were not provided."})
    return wrapper 

def validate_composite_primary_keys(db_model, *keys):
    """TODO: add description"""
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
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
