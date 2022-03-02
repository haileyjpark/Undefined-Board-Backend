from core.utils import MyAuthentication
from postings.permissions import IsOwnerOrReadOnly
from .models import Post
from users.models import User
from .serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)