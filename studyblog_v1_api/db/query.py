from typing import Any
from django.db import connection


def execute(query, *args, **kwargs) -> list[dict[str, Any]]:
    cursor = connection.cursor()
    result = cursor.execute(query, *args, **kwargs)
    return serialize_query(cursor, result)

def serialize_query(cursor, result):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, obj)) for obj in result]

# Queries

base_user_details_query = """
    SELECT 
        ur.user_id, u.username, ur.role_id, r.role_name 
    FROM 
        studyblog_v1_api_userrolemodel ur
    JOIN 
        studyblog_v1_api_rolemodel r ON ur.role_id = r.id
    JOIN
        studyblog_v1_api_userprofilemodel u ON u.id = ur.user_id
"""

def fetch_all_user_details(user_id=None) -> str:
    if isinstance(user_id, int):
        single_user_query = f"{base_user_details_query} WHERE ur.user_id = {user_id}"
        return single_user_query
    
    if isinstance(user_id, list) or isinstance(user_id, tuple):
        multiple_user_query = f"{base_user_details_query} WHERE ur.user_id IN("
        for i, id in enumerate(user_id):
            if i == 0:
                multiple_user_query += f"{id}"
                continue
            multiple_user_query += f",  {id}"

        multiple_user_query += ")"
        return multiple_user_query

    return base_user_details_query