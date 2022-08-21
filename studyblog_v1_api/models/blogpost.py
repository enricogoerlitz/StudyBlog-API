from datetime import datetime
from django.db import models
from django.conf import settings


class BlogPostModel(models.Model):
    """DB Model for storing blogposts of users"""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
    )
    title = models.CharField(max_length=50, blank=False, unique=True)
    content = models.CharField(max_length=2000, blank=False)
    created = models.DateTimeField(default=datetime.now, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        """returns model as string"""
        return f"title: {self.title[:5]}... | Content: {self.content[:10]}..."


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
    created = models.DateTimeField(default=datetime.now, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        """returns model as string"""
        return f"{self.content[:8]}..."