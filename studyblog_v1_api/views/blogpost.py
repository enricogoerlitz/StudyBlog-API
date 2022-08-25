from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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
from studyblog_v1_api.services import blogpost_service


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
            return Response(result)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            return Response(blogpost_service.get_item(request, pk))
        except ObjectDoesNotExist as exp:
            return res.error_400_bad_request(f"BlogPost object with id {pk} does not exist.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def update(self, request, pk, *args, **kwargs):
        try:
            updated_blogpost = blogpost_service.update_item(request, pk)
            return Response(updated_blogpost, status=status.HTTP_202_ACCEPTED)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
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

    def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        # details = request.query_params.get("details")
        # if details and details.lower() == "true":
        #     # error handling
        #     return Response()

        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, pk, *args, **kwargs):
        #return Response(blogpost_service.get_item(request, pk))
        # request.data.get(user_id)
        return super().retrieve(request, pk, *args, **kwargs)
    
    def update(self, request, pk, *args, **kwargs):
        # try catch etc
        current_blogpost_comment = BlogPostCommentModel.objects.filter(id=pk).values()[0]

        request.data[DB_FIELD_BLOGPOST] = current_blogpost_comment[DB_FIELD_BLOGPOST_ID]
        request.data[DB_FIELD_BLOGPOST_COMMENT] = current_blogpost_comment[DB_FIELD_BLOGPOST_COMMENT_ID]
        request.data[DB_FIELD_CREATED] = current_blogpost_comment[DB_FIELD_CREATED]
        request.data[DB_FIELD_USER] = current_blogpost_comment[DB_FIELD_USER_ID]
        return super().update(request, pk, *args, **kwargs) # selfmade!
