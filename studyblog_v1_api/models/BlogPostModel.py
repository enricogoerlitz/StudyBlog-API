from django.db import models
from django.conf import settings


DB_FIELD_USER_ID = "user_id"
DB_FIELD_TITLE = "title"
DB_FIELD_CONTENT = "content"
DB_FIELD_CREATED = "created"
DB_FIELD_LAST_EDIT = "last_edit"


class BlogPostModel(models.Model):
    """DB Model for storing blogposts of users"""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
    )
    title = models.CharField(max_length=50, blank=False, unique=True)
    content = models.CharField(max_length=2000, blank=False)
    created = models.DateTimeField(auto_now=True)
    last_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        """returns model as string"""
        return f"title: {self.title[:5]}... | Content: {self.content[:10]}..."
