from studyblog_v1_api.serializers import serializer
from studyblog_v1_api.models import (
    UserRoleModel, 
    DB_FIELD_USER_ID, 
    DB_FIELD_ROLE_ID,
    DB_FIELD_USER,
    DB_FIELD_ROLE
)


def create_item(request):
    user_id, role_id = _get_user_role_data(request)

    _validate_existing(user_id, role_id)

    new_user_role = UserRoleModel.objects.create(user_id=user_id, role_id=role_id)
    new_user_role.save()

    return serializer.model_to_json(new_user_role)


def update_item(request, pk):
    user_id, role_id = _get_user_role_data(request)
    _validate_existing(user_id, role_id)

    current_user_role = UserRoleModel.objects.get(id=pk)
    current_user_role.user_id = user_id
    current_user_role.role_id = role_id
    current_user_role.save()

    return serializer.model_to_json(current_user_role)


def _get_user_role_data(request):
    user_id = request.data.get(DB_FIELD_USER_ID) or request.data.get(DB_FIELD_USER)
    role_id = request.data.get(DB_FIELD_ROLE_ID) or request.data.get(DB_FIELD_ROLE)
    _validate_data(user_id, role_id)

    return user_id, role_id


def _validate_data(user_id, role_id):
    if user_id and role_id: return
    if user_id is None and role_id:
        raise ValueError("The field user_id is required.")
    
    if role_id is None and user_id:
        raise ValueError("The field role_id is required.")
    
    raise ValueError("The fields user_id and role_id are required.")


def _validate_existing(user_id, role_id):
    is_existing = UserRoleModel.objects.filter(user_id=user_id, role_id=role_id).exists()
    if is_existing:
        error_msg = f"Duplicate Key Error. The user with the id {user_id} already has the role with the id {role_id}"
        raise ValueError(error_msg)
