""""""

from studyblog_v1_api.db import query
from studyblog_v1_api.utils import type_check


def is_authenticated(request):
    return request.user.is_authenticated


def isin_role(request, auth_roles, auth_way="or"):
    _validate_isin_role_inputs(request, auth_roles, auth_way)
    is_list = type_check.is_list_or_tuple(auth_roles)
    user_roles = query.fetch_execute_user_roles(request.user.id)

    if auth_way == "or":
        if is_list:
            for role in auth_roles:
                if role in user_roles:
                    return True
            return False

        if auth_roles in user_roles:
            return True
        return False
    
    if is_list:
        for role in auth_roles:
            if not role in user_roles:
                return True
        return False

    if auth_roles in user_roles:
        return True
    return False


def _validate_isin_role_inputs(request, auth_roles, auth_way):
    if not is_authenticated(request):
        raise Exception("User is not authenticated!")

    if not auth_roles:
        raise ValueError("You need to pass any roles to this function.")
    
    if not auth_way in "or and":
        raise ValueError("The auth_way must be 'or' or 'and'.")
    
    if type_check.is_list_or_tuple(auth_roles):
        if len(auth_roles) == 0:
            raise ValueError(f"The length of the roles list is 0.")
    elif not isinstance(auth_roles, str):
        raise TypeError("No valid roles passed. Please pass one role as string or multiple roles as list of strings.")

