from django.urls import path, include
from .views import PostViewSet, CommentViewSet, #PostLikeViewSet, CommentLikeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('postings', PostViewSet)
# router.register('comment_likes', CommentLikeViewSet)
# router.register('post_likes', PostLikeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
