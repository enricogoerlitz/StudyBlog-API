"""
Module for custom db filter queries.
"""

from studyblog_v1_api.db import query


base_user_details_query = """
    SELECT 
        ur.user_id, u.username, ur.role_id, r.role_name, u.is_superuser, u.is_staff
    FROM 
        studyblog_v1_api_userrolemodel ur
    JOIN 
        studyblog_v1_api_rolemodel r ON ur.role_id = r.id
    JOIN
        studyblog_v1_api_userprofilemodel u ON u.id = ur.user_id
"""


def fetch_all_user_details(user_id=None) -> str:
    # TODO: more details
    if isinstance(user_id, int):
        single_user_query = f"{base_user_details_query} WHERE ur.user_id = {user_id}"
        return single_user_query
    
    if isinstance(user_id, list) or isinstance(user_id, tuple):
        multiple_user_query = f"{base_user_details_query} WHERE ur.user_id IN("
        for i, id in enumerate(user_id):
            if i == 0:
                multiple_user_query += f"{id}"
                continue
            multiple_user_query += f", {id}"

        multiple_user_query += ")"
        return multiple_user_query

    return base_user_details_query

base_user_details_query_2 = """
    SELECT 
        u.id, u.username, u.is_superuser, u.is_staff, r.role_name
    FROM 
        studyblog_v1_api_userprofilemodel u
    LEFT JOIN 
        studyblog_v1_api_userrolemodel ur ON u.id = ur.user_id
    LEFT JOIN 
        studyblog_v1_api_rolemodel r ON ur.role_id = r.id
"""

#----


base_blogpost_details_query = """
    SELECT 
        bpm.id, bpm.content, bpm.user_id, u.username, ur.role_id, r.role_name, u.is_superuser, u.is_staff, bpm.created, bpm.last_edit
    FROM 
        studyblog_v1_api_blogpostmodel bpm
    JOIN 
        studyblog_v1_api_userprofilemodel u ON bpm.user_id = u.id
    JOIN
        studyblog_v1_api_userrolemodel ur ON bpm.user_id = ur.user_id
    JOIN 
        studyblog_v1_api_rolemodel r ON ur.role_id = r.id
"""


def fetch_all_blogpost_details() -> str:
    # TODO: more details
    return base_blogpost_details_query


base_blogpost_details_query_2 = """
    SELECT 
        bp.id AS blogpost_id,
        bp.title AS blogpost_title, 
        bp.content AS blogpost_content,
        bp.created AS blogpost_created, 
        bp.last_edit AS blogpost_last_edit,

        ubp.id AS creator_id, 
        ubp.username AS creator_username,
        rbp.role_name AS creator_role_name,
        ubp.is_superuser AS creator_is_superuser, 
        ubp.is_staff AS creator_is_staff,

        bpc.id AS comment_id, 
        bpc.content AS comment_content, 
        bpc.blogpost_comment_id AS responded_comment_id,
        bpc.created AS comment_created, 
        bpc.last_edit AS comment_last_edit,

        ubpc.id AS comment_creator_id, 
        ubpc.username AS comment_creator_username, 
        rbpc.role_name AS comment_creator_role_name,
        ubpc.is_superuser AS comment_creator_is_superuser, 
        ubpc.is_staff AS comment_creator_is_staff
    FROM 
        studyblog_v1_api_blogpostmodel bp 
    LEFT JOIN 
        studyblog_v1_api_blogpostcommentmodel bpc ON bp.id = bpc.blogpost_id
    LEFT JOIN 
        studyblog_v1_api_userprofilemodel ubp ON bp.user_id = ubp.id
    LEFT JOIN 
        studyblog_v1_api_userprofilemodel ubpc ON bpc.user_id = ubpc.id
    LEFT JOIN 
        studyblog_v1_api_userrolemodel urbp ON ubp.id = urbp.user_id
    LEFT JOIN 
        studyblog_v1_api_userrolemodel urbpc ON ubpc.id = urbpc.user_id
    LEFT JOIN
        studyblog_v1_api_rolemodel rbp ON urbp.role_id = rbp.id
    LEFT JOIN
        studyblog_v1_api_rolemodel rbpc ON urbpc.role_id = rbpc.id
    ORDER BY bp.created
"""


base_is_in_role_query = """
    SELECT 
        r.role_name
    FROM 
        studyblog_v1_api_userrolemodel ur
    JOIN
        studyblog_v1_api_userprofilemodel u ON ur.user_id = u.id
    JOIN
        studyblog_v1_api_rolemodel r ON ur.role_id = r.id
    WHERE 
        u.id = 
"""

def fetch_user_roles(id) -> str:
    return f"{base_is_in_role_query}{id}"


def fetch_execute_user_roles(id) -> list[str]:
    return query.execute(
        fetch_user_roles(id), 
        formatter_func=lambda _, result: [obj[0] for obj in result]
    )