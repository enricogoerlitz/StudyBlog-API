# mypy: ignore-errors
"""
API-Endpoints for BlogPost and BlogPostComment models.
"""

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from studyblog_v1_api.utils import response as res
from studyblog_v1_api.serializers import BlogPostSerializer
from studyblog_v1_api.permissions import BlogPostPermission
from studyblog_v1_api.models import BlogPostCommentModel, BlogPostModel
from studyblog_v1_api.services import blogpost_service, blogpost_comment_service


class BlogPostViewSet(ModelViewSet):
    """Handle BlogPost CRUD-Operations"""
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, BlogPostPermission,)

    def list(self, request: Request, *args, **kwargs):
        """
        Handle GET requests.
        /api/v1/blogpost/
        /api/v1/blogpost/?details=true&blogpost_id=1,2,4
        """
        try:
            result = blogpost_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request: Request, pk: int, *args, **kwargs):
        """
        Handle GET by ID requests.
        /api/v1/blogpost/{id}
        /api/v1/blogpost/{id}/details=true
        """
        try:
            return res.success(blogpost_service.get_item(request, pk))
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPost object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
        
    def create(self, request: Request, *args, **kwargs):
        """Handle POST requests."""
        request.data["user"] = self.request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, pk: int, *args, **kwargs):
        """Handle PUT|PATCH requests."""
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

    def list(self, request: Request, *args, **kwargs):
        """
        Handle GET requests.
        /api/v1/blogpost-comment/
        /api/v1/blogpost-comment/?details=true&blogpost_id=1,2,4
        """
        try:
            result = blogpost_comment_service.get_item_list(request)
            return res.success(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def retrieve(self, request: Request, pk: int, *args, **kwargs):
        """
        Handle GET by ID requests.
        /api/v1/blogpost-comment/{id}
        /api/v1/blogpost-comment/{id}/details=true
        """
        try:
            result = blogpost_comment_service.get_item(request, pk)
            return res.success(result)
        except ObjectDoesNotExist:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def update(self, request: Request, pk: int, *args, **kwargs):
        """Handle PUT|PATCH requests."""
        try:
            result = blogpost_comment_service.update_item(request, pk)
            return res.updated(result)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except ObjectDoesNotExist as exp:
            return res.error_400_bad_request(f"BlogPostComment object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)