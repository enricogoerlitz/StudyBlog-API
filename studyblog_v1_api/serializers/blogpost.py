"""
Module for handling BlogPost serializer.
"""

from rest_framework.serializers import ModelSerializer

from studyblog_v1_api.models import (
    BlogPostModel,
    BlogPostCommentModel,
    DB_FIELD_ALL,
)


class BlogPostSerializer(ModelSerializer):
    """Serialize BlogPostModel"""
    
    class Meta:
        model = BlogPostModel
        fields = DB_FIELD_ALL


class BlogPostCommentSerializer(ModelSerializer):
    """Serialize BlogPostCommentModel"""
    
    class Meta:
        model = BlogPostCommentModel
        fields = DB_FIELD_ALL