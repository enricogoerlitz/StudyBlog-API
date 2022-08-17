from django.urls import path, include
from rest_framework.routers import DefaultRouter
from studyblog_v1_api import views


router = DefaultRouter()
router.register("profile", views.UserProfileViewSet)

urlpatterns = [
    path("test", views.TestApiView.as_view()),
    path("login/", views.ProfileLoginApiView.as_view()),
    path("", include(router.urls))
]
