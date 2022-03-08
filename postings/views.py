from core.utils import MyAuthentication
from postings.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, PostLike, CommentLike
from users.models import User
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from rest_framework import status, viewsets
from rest_framework.response   import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter


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


class PostLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        obj = PostLike.objects.filter(user=user, post=request.data['post'])
        like_count = PostLike.objects.filter(post_id=request.data['post']).count()
        if obj.exists():
            obj.delete()
            return Response({"Message" : "Like Cancelled", "like_count" : like_counts}, status=status.HTTP_200_OK)
        
        request.data['user'] = User.objects.get(email=request.user).id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer_data = serializer.data 
        serializer_data['like_count'] = like_count
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)        
        

class CommentLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    http_method_names = ['post']
    
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        obj = CommentLike.objects.filter(user=user, comment=request.data['comment'])
        like_count = CommentLike.objects.filter(comment_id=request.data['comment']).count()
        if obj.exists():
            obj.delete()
            return Response({"Message" : "Like Cancelled", "like_count" : like_count}, status=status.HTTP_200_OK)
        
        request.data['user'] = User.objects.get(email=request.user).id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer_data = serializer.data 
        serializer_data['like_count'] = like_count
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)