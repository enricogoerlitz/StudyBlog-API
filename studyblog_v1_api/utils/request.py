"""Middleware"""

from rest_framework.response import Response
from rest_framework import status

from studyblog_v1_api.db import query


class ValidDataWrapper:
    def __init__(self, data, error_msg=None):
        if data is None and error_msg is None:
            raise ValueError("You need to add an error message, if the data is None")

        self.data = data
        self.is_valid = not data is None
        self.errors = error_msg


def get_id_obj(model, Serializer, auto_exe=True):
    """
    Checks, whether an id was passed the a get request.

    Args:
        model (DB_Model): an DB Model
        Serializer (Model Serializer): an Model serializer to serialize the model
    """
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            #request = args[0]
            id = request.query_params.get("id")
            if not id:
                return func(view, *args, **kwargs)

            try:
                obj = model.objects.get(pk=id)
                id_obj = Serializer(obj, many=False).data

                if auto_exe:
                    return Response(id_obj)

                return func(view, request, ValidDataWrapper(id_obj), *args, **kwargs)
            except Exception:
                err_msg = f"Could not find an object with the id {id}"
                if auto_exe:
                    return Response({"error": err_msg}, status=status.HTTP_400_BAD_REQUEST)

                return func(view, request, ValidDataWrapper(None, err_msg), *args, **kwargs)
        return wrapper
    return decorator

def isin_role(auth_roles, auth_way="or"): 
    """_summary_

    Args:
        auth_roles (_type_): _description_
        auth_way (str, optional): "or" | "and".
    """
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise Exception("User is not authenticated!")

            if not auth_roles:
                raise ValueError("You need to pass any roles to this function.")
            
            if not auth_way in "or and":
                raise ValueError("The auth_way must be 'or' or 'and'.")
            
            is_list = False
            if isinstance(auth_roles, list) or isinstance(auth_roles, tuple):
                if len(auth_roles) == 0:
                    raise ValueError(f"The length of the roles list is 0.")
                is_list = True
            
            if not is_list and not isinstance(auth_roles, str):
                raise TypeError("No valid roles passed. Please pass one role as string or multiple roles as list of strings.")

            user_roles = query.fetch_execute_user_roles(request.user.id)

            access_denied_response = Response({"error": "Access denied. User hasn't the needed permission to access this resource."}, status=status.HTTP_401_UNAUTHORIZED)
            access_granted_response = lambda: func(view, request, *args, **kwargs)
            if auth_way == "or":
                if is_list:
                    for role in auth_roles:
                        if role in user_roles:
                            return access_granted_response()
                    return access_denied_response

                if auth_roles in user_roles:
                    return access_granted_response()
                return access_denied_response
            
            if is_list:
                for role in auth_roles:
                    if not role in user_roles:
                        return access_denied_response
                return access_granted_response()

            if auth_roles in user_roles:
                return access_granted_response()
            return access_denied_response
        return wrapper
    return decorator

                
def is_authenticated(func):
    def wrapper(view, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(view, request, *args, **kwargs)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper 



def validate_composite_primary_keys(keys, table):
    # extract keys values form query_params with the 'keys' above given
    # arr = ["user_id", "role_id"] -> in func query_params -> d = {column: request.query_params.get(columns) for column in arr}
    # Model.objects.filter(**d).count() > 0 -> return error-response
    pass