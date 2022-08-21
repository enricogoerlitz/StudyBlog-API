SELECT 
    ur.user_id, u.username, ur.role_id, r.role_name 
FROM 
    studyblog_v1_api_userrolemodel ur
JOIN 
    studyblog_v1_api_rolemodel r ON ur.role_id = r.id
JOIN
    studyblog_v1_api_userprofilemodel u ON u.id = ur.user_id;