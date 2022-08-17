from django.urls import path
import studyblog_v1_api.views as views

urlpatterns = [
    path("test", views.TestApiView.as_view())
]
