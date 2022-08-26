from django.core.exceptions import ObjectDoesNotExist

from studyblog_v1_api.models import BlogPostModel
from studyblog_v1_api.serializers import serializer
from studyblog_v1_api.db import query, filter
from studyblog_v1_api.models import (
    DB_FIELD_CREATED,
    DB_FIELD_USER_ID,
    DB_FIELD_USER,
)
from studyblog_v1_api.utils.request import PUT


def get_item_list(request):
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostModel.objects.all())
    
    blogpost_data = query.execute(filter.fetch_blogpost_details())
    if len(blogpost_data) == 0: return []
    
    return _get_blogpost_items(blogpost_data)


def get_item(request, pk):
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostModel.objects.get(id=pk))

    blogpost_data = query.execute(filter.fetch_blogpost_details(pk))
    if len(blogpost_data) == 0: raise ObjectDoesNotExist()

    return _get_blogpost_obj(blogpost_data[0])
    

def update_item(request, pk):
    title = request.data.get("title")
    content = request.data.get("content")
    if not title and not content:
        raise ValueError("No title and no content where passed.")
    
    current_blogpost = BlogPostModel.objects.get(id=pk)
    if request.method == PUT and (not title or not content):
        raise ValueError("For PUT requests are the fields title and content required.")
    
    return _update_save_blogpost(current_blogpost, title, content)


def _get_blogpost_items(blogpost_data):
    result = []
    added_blogposts = {}
    added_comments = {}
    for row in blogpost_data:
        blogpost_id = row["blogpost_id"]
        comment_id = row["comment_id"]

        if not blogpost_id in added_blogposts:
            added_blogposts[blogpost_id] = len(result)
            if comment_id: added_comments[comment_id] = 0

            result.append(_get_blogpost_obj(row))
            continue

        blogpost = result[added_blogposts[blogpost_id]]
        if not row["creator_role_name"] in blogpost["creator"]["roles"]:
            blogpost["creator"]["roles"].append(row["creator_role_name"])
            continue

        if not comment_id: continue
        
        if comment_id in added_comments:
            blogpost["comments"][added_comments[comment_id]]["creator"]["roles"].append(row["comment_creator_role_name"])
            continue
        
        added_comments[comment_id] = len(blogpost["comments"])
        blogpost["comments"].append(_get_blogpost_comment_obj(row))

    return result

def _get_blogpost_obj(data):
    return {
        "id": data["blogpost_id"],
        "title": data["blogpost_title"],
        "content": data["blogpost_content"],
        "created": data["blogpost_created"],
        "last_edit": data["blogpost_last_edit"],
        "creator": {
            "id": data["creator_id"],
            "username": data["creator_username"],
            "roles": [data["creator_role_name"]],
            "is_superuser": data["creator_is_superuser"],
            "is_staff": data["creator_is_staff"],
        },
        "comments": [] if not data["comment_id"] else [_get_blogpost_comment_obj(data)]
    }

def _get_blogpost_comment_obj(data):
    return {
        "id": data["comment_id"],
        "content": data["comment_content"],
        "created": data["comment_created"],
        "responded_comment_id": data["responded_comment_id"],
        "last_edit": data["comment_last_edit"],
        "creator": {
            "id": data["comment_creator_id"],
            "username": data["comment_creator_username"],
            "roles": [data["comment_creator_role_name"]],
            "is_superuser": data["comment_creator_is_superuser"],
            "is_staff": data["comment_creator_is_staff"]
        }
    }


def _update_save_blogpost(blogpost, title, content):
    if title: blogpost.title = title
    if content: blogpost.content = content
    blogpost.save()
    return serializer.model_to_json(blogpost)