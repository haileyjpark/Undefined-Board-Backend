from core.utils import MyAuthentication
from postings.permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    filter_backends = [SearchFilter]
    search_fields = ('category__id',)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)