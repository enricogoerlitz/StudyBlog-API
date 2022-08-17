from django.db import models
from django.conf import settings
from studyblog_v1_api.models import BlogPostModel


DB_FIELD_USER_ID = "user_id"
DB_FIELD_BLOGPOST_ID = "blogpost_id"
DB_FIELD_BLOGPOST_COMMENT_ID = "blogpost_comment_id"
DB_FIELD_CONTENT = "content"
DB_FIELD_CREATED = "created"
DB_FIELD_LAST_EDIT = "last_edit"


class BlogPostCommentModel(models.Model):
    """DB Model for storing comments, related to an blogpost"""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False
    )
    blogpost = models.ForeignKey(
        to=BlogPostModel,
        on_delete=models.CASCADE,
        null=False
    )
    blogpost_comment = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True
    )
    content = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        """returns model as string"""
        return f"{self.content[:8]}..."