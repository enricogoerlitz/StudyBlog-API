from django.core.exceptions import ObjectDoesNotExist

from studyblog_v1_api.db import query, filter, roles
from studyblog_v1_api.serializers import serializer 
from studyblog_v1_api.models import (
    UserProfileModel,
    UserRoleModel,
    RoleModel,
    DB_FIELD_ROLE_ID,
    DB_FIELD_USERNAME,
    DB_FIELD_PASSWORD,
    DB_FIELD_ID
)
from studyblog_v1_api.services import role_service
from studyblog_v1_api.utils import type_check


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
        role_service.validate_role(passed_user_role_ids)
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
    
    return serializer.model_to_json(created_user, DB_FIELD_ID, DB_FIELD_USERNAME)

def get_item_list(request):
    user_ids = _get_req_user_ids(request)

    if not filter.is_details(request):
        return serializer.model_to_json(UserProfileModel.objects.all().order_by("id"), DB_FIELD_ID, DB_FIELD_USERNAME)
    
    users_data = query.execute(filter.fetch_user_details(user_ids))
    if len(users_data) == 0: return []

    return _get_user_objs(users_data)


def get_item(request, pk):
    if not filter.is_details(request):
        return serializer.model_to_json(UserProfileModel.objects.get(id=pk), DB_FIELD_ID, DB_FIELD_USERNAME)
    
    user_data = query.execute(filter.fetch_user_details(pk))
    if len(user_data) == 0: raise ObjectDoesNotExist()
    
    return _get_user_objs(user_data)[0]


def is_authenticated(request):
    return request.user.is_authenticated

def is_role_valid(role):

    pass

def isin_role(auth_roles, request=None, id=None, auth_way="or"):
    _validate_isin_role_inputs(auth_roles, request, id, auth_way)

    id = id if id else request.user.id
    is_list = type_check.is_list_or_tuple(auth_roles)
    user_roles = filter.fetch_execute_user_roles(id)

    if auth_way == "or":
        if is_list:
            for role in auth_roles:
                if role in user_roles: return True
            return False

        if auth_roles in user_roles: return True
        return False
    
    if is_list:
        for role in auth_roles:
            if not role in user_roles: return True # False?
        return False

    if auth_roles in user_roles:  return True
    return False

def _get_user_objs(users_data):
    result = []
    added_users = dict()
    for row in users_data:
        user_id = row["id"]
        if not user_id in added_users:
            added_users[user_id] = len(result)
            result.append(_get_user_obj(row))
            continue
        
        result[added_users[user_id]]["roles"].append(row["role_name"])
    return result

def _get_user_obj(user_data):
    return {
        "id": user_data["id"],
        "username": user_data["username"],
        "is_superuser": user_data["is_superuser"],
        "is_staff": user_data["is_staff"],
        "roles": [] if not user_data["role_name"] else [user_data["role_name"]],
    }

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

def _get_req_user_ids(request):
    user_ids = request.query_params.get("user_id")
    if not user_ids: return None

    user_ids = user_ids.split(",")
    for id in user_ids:
        if not type_check.is_int(id, or_float=False):
            raise ValueError(f"The passed id {id} is invalid!")
    return user_ids if len(user_ids) > 1 else user_ids[0]