from django.urls import path, include
from rest_framework.routers import DefaultRouter

from studyblog_v1_api import views


router = DefaultRouter()
router.register("user", views.UserViewSet)
router.register("role", views.RoleViewSet)
router.register("userrole", views.UserRoleViewSet)
router.register("blogpost", views.BlogPostViewSet)
router.register("blogpost-comment", views.BlogPostCommentViewSet)


urlpatterns = [
    path("test/", views.TestApiView.as_view()),
    path("login/", views.UserAuthTokenApiView.as_view()),
    path("", include(router.urls))
]
