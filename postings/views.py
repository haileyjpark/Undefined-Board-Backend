from urllib import response
from core.utils import MyAuthentication
from postings.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, PostLike, CommentLike
from .serializers import CommentLikeSerializer, PostSerializer, CommentSerializer, PostLikeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, BaseFilterBackend
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    filter_backends = [SearchFilter]
    search_fields = ('category__id',)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['post', 'patch', 'delete']
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# class PostLikeViewSet(viewsets.ModelViewSet):
#     authentication_classes = [MyAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = PostLike.objects.all()
#     serializer_class = PostLikeSerializer
#     http_method_names = ['post']
    
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)
        

# class CommentLikeViewSet(viewsets.ModelViewSet):
#     authentication_classes = [MyAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = CommentLike.objects.all()
#     serializer_class = CommentLikeSerializer
#     http_method_names = ['post']
    
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)