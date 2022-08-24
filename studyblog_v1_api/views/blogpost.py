""""""

from django.db import connection
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from studyblog_v1_api.db import query
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


class BlogPostViewSet(ModelViewSet):
    """"""
    permission_classes = (IsAuthenticated, BlogPostPermission)
    authentication_classes = (TokenAuthentication,)
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    # filter_backends = (SearchFilter, )
    # search_fields = (DB_TI)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        details = request.query_params.get("details") # to constant


        blogpost_data = query.execute(query.base_blogpost_details_query_2)

        result = []
        added_blogposts = dict()
        added_comments = dict()
        for row in blogpost_data:
            blogpost_id = row["blogpost_id"]
            #comment_id = row["comment_id"],
            if not blogpost_id in added_blogposts.keys():
                added_blogposts[blogpost_id] = len(result)
                if row["comment_id"]:
                    added_comments[row["comment_id"]] = 0
                result.append({
                    "id": row["blogpost_id"],
                    "title": row["blogpost_title"],
                    "content": row["blogpost_content"],
                    "created": row["blogpost_created"],
                    "last_edit": row["blogpost_last_edit"],
                    "creator": {
                        "id": row["creator_id"],
                        "username": row["creator_username"],
                        "roles": [row["creator_role_name"]],
                        "is_superuser": row["creator_is_superuser"],
                        "is_staff": row["creator_is_staff"],
                    },
                    "comments": [] if not row["comment_id"] else [
                        {
                            "id": row["comment_id"],
                            "content": row["comment_content"],
                            "created": row["comment_created"],
                            "responded_comment_id": row["responded_comment_id"],
                            "last_edit": row["comment_last_edit"],
                            "creator": {
                                "id": row["comment_creator_id"],
                                "username": row["comment_creator_username"],
                                "roles": [row["comment_creator_role_name"]],
                                "is_superuser": row["comment_creator_is_superuser"],
                                "is_staff": row["comment_creator_is_staff"]
                            }
                        }
                    ]
                })

                continue


            blogpost = result[added_blogposts[blogpost_id]]
            if not row["creator_role_name"] in blogpost["creator"]["roles"]:
                blogpost["creator"]["roles"].append(row["creator_role_name"])
                continue
            
            comment_id = row["comment_id"]

            if not comment_id: 
                continue
            
            if comment_id in added_comments.keys():
                blogpost["comments"][added_comments[comment_id]]["creator"]["roles"].append(row["comment_creator_role_name"])
                continue
            
            added_comments[comment_id] = len(blogpost["comments"])
            
            blogpost["comments"].append({
                "id": row["comment_id"],
                "content": row["comment_content"],
                "responded_comment_id": row["responded_comment_id"],
                "created": row["comment_created"],
                "last_edit": row["comment_last_edit"],
                "creator": {
                    "id": row["comment_creator_id"],
                    "username": row["comment_creator_username"],
                    "roles": [row["comment_creator_role_name"]],
                    "is_superuser": row["comment_creator_is_superuser"],
                    "is_staff": row["comment_creator_is_staff"]
                }
            })
        
        return Response(result)
 
        if details and details.lower() == "true":
            # WITH COMMENTS!
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
