from studyblog_v1_api.db import query, filter, roles
from studyblog_v1_api.models import UserProfileModel, UserRoleModel, RoleModel, DB_FIELD_ROLE_ID, DB_FIELD_USERNAME, DB_FIELD_PASSWORD
from studyblog_v1_api.utils import type_check


def is_authenticated(request):
    return request.user.is_authenticated


def is_role_valid():
    pass


def isin_role(auth_roles, request=None, id=None, auth_way="or"):
    _validate_isin_role_inputs(auth_roles, request, id, auth_way)

    id = id if id else request.user.id
    is_list = type_check.is_list_or_tuple(auth_roles)
    user_roles = filter.fetch_execute_user_roles(id)

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


def _validate_isin_role_inputs(auth_roles, request, id, auth_way):
    """if id is passed, the request will be ignored and it is not necessary to validate the authentication"""
    if not id and not request:
        raise ValueError("You need to pass an request or an user id.")

    if not id and not is_authenticated(request):
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


def create_user(request, validated_data):
    """Handle creating a new user"""
    passed_user_role_ids = request.data.get(DB_FIELD_ROLE_ID)
    user_roles = []
    # raise error when error
    if passed_user_role_ids and not is_authenticated(request):
        # custom exception!
        raise Exception("It was passed an role id, but only admins!")
        
    if (
        passed_user_role_ids and
        isin_role(roles.ADMIN, request=request)
    ):
        # validate roles! -> SELECT - IN() -> len() = len()
        if type_check.is_list_or_tuple(passed_user_role_ids):
            user_roles = list(passed_user_role_ids)
        else:
            user_roles.append(passed_user_role_ids)
    else:
        user_roles.append(RoleModel.objects.get(role_name=roles.STUDENT).id)

    created_user = UserProfileModel.objects.create_user(
        username=validated_data.get(DB_FIELD_USERNAME),
        password=validated_data.get(DB_FIELD_PASSWORD),
    )

    if created_user:
        for role in user_roles:
            UserRoleModel.objects.create(user_id=created_user.id, role_id=role)

    return created_user