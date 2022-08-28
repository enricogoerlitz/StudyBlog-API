"""
Service for handling BlogPostComment operations.
"""

from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.request import Request

from studyblog_v1_api.models import BlogPostCommentModel
from studyblog_v1_api.serializers import serializer
from studyblog_v1_api.db import query, filter


def get_item_list(request: Request) -> list[dict[str, Any]]:
    """
    Returns a list of blogpost comments.
    If the request query params contains the param 'details=true', it returns a list of blogpost comments with details (user and user roles).
    Otherwise only the blogpost comment data.
    """
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.all())
    
    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details())
    if len(blogpost_comment_data) == 0: return []

    return _get_blogpost_comment_items(blogpost_comment_data)


def get_item(request: Request, pk: int) -> dict[str, Any]:
    """
    Returns an serialized BlogPostComment object.
    Raises an ObjectDoesNotExist exception, if the object does not existing.
    If the request query params contains the param 'details=true', it returns the BlogpostComment with details (user and user roles).
    Otherwise only the BlogPostComment data.
    """
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.get(id=pk))

    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details(pk))
    if len(blogpost_comment_data) == 0: raise ObjectDoesNotExist()

    return _get_comment_obj(blogpost_comment_data[0])


def update_item(request: Request, pk: int) -> dict[str, Any]:
    """
    Handle updating a BlogPostComment.
    Raises an ValueError, if the 'content' is blank.
    Raises an ObjectDoesNotExits exception, if the object does not existing.
    """
    content = request.data.get("content")
    if not content: raise ValueError("Field content is required.")
    
    current_blogpost_comment = BlogPostCommentModel.objects.get(id=pk)
    current_blogpost_comment.content = content
    current_blogpost_comment.save()

    return serializer.model_to_json(current_blogpost_comment)


def _get_blogpost_comment_items(blogpost_comment_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Returns a prepared list of detailed BlogPostComments."""
    result: list[dict[str, Any]] = []
    added_comments = {}
    for row in blogpost_comment_data:
        comment_id = row["id"]
        if not comment_id in added_comments:
            added_comments[comment_id] = len(result)
            result.append(_get_comment_obj(row))
            continue
        
        result[added_comments[comment_id]]["creator"]["roles"].append(row["role_name"])
    
    return result


def _get_comment_obj(data) -> dict[str, Any]:
    """Returns a detailed BlogPostComment object."""
    return {
        "id": data["id"],
        "content": data["content"],
        "blogpost_id": 5,
        "responded_comment_id": data["blogpost_comment_id"],
        "created": data["created"],
        "last_edit": data["last_edit"],
        "creator": {
            "id": data["user_id"],
            "username": data["username"],
            "roles": [data["role_name"]],
            "is_superuser": data["is_superuser"],
            "is_staff": data["is_staff"]
        }
    }