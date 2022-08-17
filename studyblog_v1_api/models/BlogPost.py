from django.db import models
from django.conf import settings


class BlogPost(models.Model):
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
