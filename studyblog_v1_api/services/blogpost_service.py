"""
Service for handling BlogPost operations.
"""

from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

from rest_framework.request import Request

from studyblog_v1_api.models import BlogPostModel
from studyblog_v1_api.serializers import serializer
from studyblog_v1_api.db import query, filter
from studyblog_v1_api.middleware.request import PUT


def get_item_list(request: Request) -> list[dict[str, Any]]:
    """
    Returns a list of blogposts.
    If the request query params contains the param 'details=true', it returns a list of blogposts with details (user, user roles and comments).
    Otherwise only the blogpost data.
    """
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostModel.objects.all())
    
    blogpost_data = query.execute(filter.fetch_blogpost_details())
    if len(blogpost_data) == 0: return []
    
    return _get_blogpost_items(blogpost_data)


def get_item(request: Request, pk: int) -> dict[str, Any]:
    """
    Returns an serialized BlogPost object.
    Raises an ObjectDoesNotExist exception, if the object does not existing.
    If the request query params contains the param 'details=true', it returns the Blogpost with details (user, user roles and comments).
    Otherwise only the BlogPostComment data.
    """
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostModel.objects.get(id=pk))

    blogpost_data = query.execute(filter.fetch_blogpost_details(pk))
    if len(blogpost_data) == 0: raise ObjectDoesNotExist()

    return _get_blogpost_obj(blogpost_data[0])
    

def update_item(request: Request, pk: int) -> dict[str, Any]:
    """
    Handle updating a BlogPost.
    Raises an ValueError, if the 'title' and the 'content' is blank.
    Raises an ValueError, of the request method is put and the 'title' or the 'content' is blank.
    Raises an ObjectDoesNotExits exception, if the object does not existing.
    """
    title = request.data.get("title")
    content = request.data.get("content")
    if not title and not content:
        raise ValueError("No title and no content where passed.")
    
    current_blogpost = BlogPostModel.objects.get(id=pk)

    if request.method == PUT and (not title or not content):
        raise ValueError("For PUT requests are the fields title and content required.")
    
    return _update_save_blogpost(current_blogpost, title, content)


def _get_blogpost_items(blogpost_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Returns a prepared list of detailed BlogPosts."""
    result: list[dict[str, Any]] = []
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


def _get_blogpost_obj(data: dict[str, Any]) -> dict[str, Any]:
    """Returns a detailed BlogPost object."""
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


def _get_blogpost_comment_obj(data: dict[str, Any]) -> dict[str, Any]:
    """Returns a detailed BlogPostComment object."""
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


def _update_save_blogpost(blogpost: Model, title: str, content: str) -> dict[str, Any]:
    """Handle generic updating and saving BlogPost."""
    if title: blogpost.title = title
    if content: blogpost.content = content
    blogpost.save()
    
    return serializer.model_to_json(blogpost)