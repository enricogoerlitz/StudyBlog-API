""""""

from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from studyblog_v1_api.db import query
from studyblog_v1_api.serializers import BlogPostCommentSerializer, BlogPostSerializer
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


class BlogPostViewSet(ModelViewSet):
    """"""
    #permission_classes = ()
    #authentication_classes = (TokenAuthentication,)
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    # filter_backends = (SearchFilter, )
    # search_fields = (DB_TI)

    def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        details = request.query_params.get("details") # to constant
        if details and details.lower() == "true":
            return Response(query.execute(query.fetch_all_blogpost_details()))

        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    def update(self, request, pk, *args, **kwargs):
        # try catch etc
        current_blogpost = BlogPostModel.objects.filter(id=pk).values()[0]
        request.data[DB_FIELD_CREATED] = current_blogpost[DB_FIELD_CREATED]
        request.data[DB_FIELD_USER] = current_blogpost[DB_FIELD_USER_ID]
        
        return super().update(request, pk, *args, **kwargs) # selfmade!


class BlogPostCommentViewSet(ModelViewSet):
    """"""
    #permission_classes = ()
    #authentication_classes = (TokenAuthentication, )
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
