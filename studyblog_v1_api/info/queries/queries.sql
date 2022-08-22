-- SQLite
-- SQLite
-- SQLite
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

SELECT 
    * 
FROM 
    studyblog_v1_api_blogpostcommentmodel bpc
CROSS JOIN 
    studyblog_v1_api_blogpostcommentmodel self_bpc ON bpc.id = self_bpc.blogpost_comment_id
SELECT * FROM studyblog_v1_api_userrolemodel
SELECT 
    * 
FROM 
    studyblog_v1_api_blogpostcommentmodel bpc
LEFT JOIN 
    studyblog_v1_api_blogpostcommentmodel self_bpc ON bpc.id = self_bpc.blogpost_comment_id

-- SQLite
SELECT 
    bp.id AS blogpost_id,
    bp.title AS blogpost_title, 
    bp.content AS blogpost_content,
    bp.created AS blogpost_created, 
    bp.last_edit AS blogpost_last_edit,

    ubp.id AS creator_id, 
    ubp.username AS creator_username, 
    ubp.is_superuser AS creator_is_superuser, 
    ubp.is_staff AS creator_is_staff,

    bpc.id AS comment_id, 
    bpc.content AS comment_content, 
    bpc.created AS comment_created, 
    bpc.last_edit AS comment_last_edit,
    
    ubpc.id AS comment_creator_id, 
    ubpc.username AS comment_creator_username, 
    ubpc.is_superuser AS comment_creator_is_superuser, 
    ubpc.is_staff AS comment_creator_is_staff
FROM 
    studyblog_v1_api_blogpostmodel bp 
JOIN 
    studyblog_v1_api_blogpostcommentmodel bpc ON bp.id = bpc.blogpost_id
JOIN 
    studyblog_v1_api_userprofilemodel ubp ON bp.user_id = ubp.id
JOIN 
    studyblog_v1_api_userprofilemodel ubpc ON bpc.user_id = ubpc.id
JOIN 
    studyblog_v1_api_userrolemodel urbp ON ubp.id = urbp.user_id
JOIN 
    studyblog_v1_api_userrolemodel urbpc ON ubpc.id = urbpc.user_id
JOIN
    studyblog_v1_api_rolemodel rbp ON urbp.role_id = rbp.id
JOIN
    studyblog_v1_api_rolemodel rbpc ON urbpc.role_id = rbpc.id
ORDER BY bp.created

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


SELECT 
    u.id, u.username, u.is_superuser, u.is_staff, r.role_name
FROM 
    studyblog_v1_api_userprofilemodel u
LEFT JOIN 
    studyblog_v1_api_userrolemodel ur ON u.id = ur.user_id
LEFT JOIN 
    studyblog_v1_api_rolemodel r ON ur.role_id = r.id