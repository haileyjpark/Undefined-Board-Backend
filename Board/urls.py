from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from postings import *
from postings import views

schema_view = get_schema_view(
    openapi.Info(
        title="CRUD API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r"postings", views.PostViewSet, basename="postings")
router.register(r"comments", views.CommentViewSet, basename="comments")
router.register(r"post_likes", views.PostLikeViewSet, basename="post_likes")
router.register(r"comment_likes", views.CommentLikeViewSet, basename="comment_likes")



urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path("", include('postings.urls')),
    # path("users/", include('dj_rest_auth.urls')),
    # path("users/", include('allauth.urls')),
    path("users/", include('users.urls')),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
