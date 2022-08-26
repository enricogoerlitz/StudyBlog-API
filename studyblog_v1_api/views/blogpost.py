from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from studyblog_v1_api.db import query, filter
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.serializers import BlogPostCommentSerializer, BlogPostSerializer
from studyblog_v1_api.permissions import BlogPostPermission
from studyblog_v1_api.models import (
    BlogPostCommentModel, 
    BlogPostModel,
    DB_FIELD_CREATED,
    DB_FIELD_USER,
    DB_FIELD_USER_ID,
    DB_FIELD_BLOGPOST_COMMENT,
    DB_FIELD_BLOGPOST_COMMENT_ID,
    DB_FIELD_BLOGPOST,
    DB_FIELD_BLOGPOST_ID,
)
from studyblog_v1_api.services import blogpost_service, blogpost_comment_service


class BlogPostViewSet(ModelViewSet):
    """Handle BlogPost CRUD-Operations"""
    permission_classes = (IsAuthenticated, BlogPostPermission)
    authentication_classes = (TokenAuthentication,)
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    # filter_backends = (SearchFilter, )
    # search_fields = (DB_TI)

    def perform_create(self, serializer):
        #try-catch -> how Response? -> alternativ zu POST?:
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            result = blogpost_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            return res.success(blogpost_service.get_item(request, pk))
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPost object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def update(self, request, pk, *args, **kwargs):
        try:
            updated_blogpost = blogpost_service.update_item(request, pk)
            return res.updated(updated_blogpost)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPost object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)


class BlogPostCommentViewSet(ModelViewSet):
    """Handle BlogPostComment CRUD-Operations"""

    permission_classes = (IsAuthenticated, BlogPostPermission)
    authentication_classes = (TokenAuthentication, )
    serializer_class = BlogPostCommentSerializer
    queryset = BlogPostCommentModel.objects.all()
    # filter_backends = (SearchFilter, )
    # search_fields = (DB_TI)

    def list(self, request, *args, **kwargs):
        try:
            result = blogpost_comment_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            result = blogpost_comment_service.get_item(request, pk)
            return res.success(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def update(self, request, pk, *args, **kwargs):
        try:
            result = blogpost_comment_service.update_item(request, pk)
            return res.updated(result)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except ObjectDoesNotExist as exp:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
