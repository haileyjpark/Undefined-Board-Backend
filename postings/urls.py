from django.urls import path, include
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('postings', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
