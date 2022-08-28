"""TODO: add description"""

from django.core.exceptions import ObjectDoesNotExist

from studyblog_v1_api.models import BlogPostCommentModel
from studyblog_v1_api.serializers import BlogPostCommentSerializer, serializer
from studyblog_v1_api.db import query, filter


def get_item_list(request):
    """TODO: add description"""
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.all())
    
    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details())
    if len(blogpost_comment_data) == 0: return []

    return _get_blogpost_comment_items(blogpost_comment_data)

def get_item(request, pk):
    """TODO: add description"""
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.get(id=pk))

    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details(pk))
    if len(blogpost_comment_data) == 0: raise ObjectDoesNotExist()

    return _get_comment_obj(blogpost_comment_data[0])

def update_item(request, pk):
    """TODO: add description"""
    content = request.data.get("content")
    if not content:
        raise ValueError("Field content is required.")
    
    current_blogpost_comment = BlogPostCommentModel.objects.get(id=pk)
    current_blogpost_comment.content = content
    current_blogpost_comment.save()

    return serializer.model_to_json(current_blogpost_comment)

def _get_blogpost_comment_items(blogpost_comment_data):
    """TODO: add description"""
    result = []
    added_comments = {}
    for row in blogpost_comment_data:
        comment_id = row["id"]
        if not comment_id in added_comments:
            added_comments[comment_id] = len(result)
            result.append(_get_comment_obj(row))
            continue
        
        result[added_comments[comment_id]]["creator"]["roles"].append(row["role_name"])
    
    return result

def _get_comment_obj(data):
    """TODO: add description"""
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
