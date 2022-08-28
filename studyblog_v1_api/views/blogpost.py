"""TODO: add description"""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from studyblog_v1_api.db import query, filter
from studyblog_v1_api.utils import response as res
from studyblog_v1_api.serializers import BlogPostCommentSerializer, BlogPostSerializer
from studyblog_v1_api.permissions import BlogPostPermission
from studyblog_v1_api.models import BlogPostCommentModel, BlogPostModel
from studyblog_v1_api.services import blogpost_service, blogpost_comment_service


class BlogPostViewSet(ModelViewSet):
    """Handle BlogPost CRUD-Operations"""
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, BlogPostPermission,)

    def list(self, request, *args, **kwargs):
        """TODO: add description"""
        try:
            result = blogpost_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            return res.success(blogpost_service.get_item(request, pk))
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPost object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
        
    def create(self, request, *args, **kwargs):
        """TODO: add description"""
        request.data["user"] = self.request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
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
    queryset = BlogPostCommentModel.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, BlogPostPermission)

    def list(self, request, *args, **kwargs):
        """TODO: add description"""
        try:
            result = blogpost_comment_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            result = blogpost_comment_service.get_item(request, pk)
            return res.success(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def update(self, request, pk, *args, **kwargs):
        """TODO: add description"""
        try:
            result = blogpost_comment_service.update_item(request, pk)
            return res.updated(result)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except ObjectDoesNotExist as exp:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
