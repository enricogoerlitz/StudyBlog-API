from django.core.exceptions import ObjectDoesNotExist

from studyblog_v1_api.models import BlogPostCommentModel
from studyblog_v1_api.serializers import BlogPostCommentSerializer, serializer
from studyblog_v1_api.db import query, filter


def get_item_list(request):
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.all())
    
    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details())
    if len(blogpost_comment_data) == 0: return []

    return [_get_comment_obj(comment) for comment in blogpost_comment_data]


def get_item(request, pk):
    if not filter.is_details(request):
        return serializer.model_to_json(BlogPostCommentModel.objects.get(id=pk))

    blogpost_comment_data = query.execute(filter.fetch_blogpost_comment_details(pk))
    if len(blogpost_comment_data) == 0: raise ObjectDoesNotExist()

    return _get_comment_obj(blogpost_comment_data[0])


def update_item(request, pk):
    content = request.data.get("content")
    if not content:
        raise ValueError("Field content is required.")
    
    current_blogpost_comment = BlogPostCommentModel.objects.get(id=pk)
    current_blogpost_comment.content = content
    current_blogpost_comment.save()

    return serializer.model_to_json(current_blogpost_comment)


def _get_comment_obj(data):
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
