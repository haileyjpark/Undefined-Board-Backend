from datetime import datetime
from django.utils import timezone
from core.utils import MyAuthentication
from postings.permissions import AllowAny, IsOwnerOrReadOnly
from .models import Post, Comment, PostLike, CommentLike
from users.models import User
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from rest_framework import status, viewsets
from rest_framework.response   import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction


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
        
    def retrieve(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        tomorrow = datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.COOKIES.get('hit') is not None:
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|')
            if str(pk) not in cookies_list:
                response.set_cookie('hit', cookies+f'|{pk}', expires=expires)
                with transaction.atomic():
                    instance.viewer += 1
                    instance.save()
                    
        else:
            response.set_cookie('hit', pk, expires=expires)
            instance.viewer += 1
            instance.save()
            
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        return response
                    
        
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
            return Response({"Like" : False, "like_count" : like_count}, status=status.HTTP_200_OK)
        
        request.data['user'] = User.objects.get(email=request.user).id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Like" : True, "like_count" : like_count}, status=status.HTTP_201_CREATED, headers=headers)        
        

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
            return Response({"Like" : False, "like_count" : like_count}, status=status.HTTP_200_OK)
        
        request.data['user'] = User.objects.get(email=request.user).id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Like" : True, "like_count" : like_count}, status=status.HTTP_201_CREATED, headers=headers)
    

class PostSearchView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get']
    
    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('tag', openapi.IN_QUERY, "search tags", type=openapi.TYPE_STRING),
    openapi.Parameter('search', openapi.IN_QUERY, "search contents", type=openapi.TYPE_STRING,
                      required=False, collection_format='multi'),])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.set_filters(self.get_queryset(), request)
        serializer = self.get_serializer(queryset, many= True)
        
        return Response(serializer.data)
    
    def set_filters(self, queryset, request):
        tag = request.query_params.get('tag', None)
        search = request.query_params.get('search', None)
        
        if tag is not None:
            if search is not None:
                queryset = Post.objects.none()
                for search_item in search.split():
                    queryset = queryset | Post.objects.filter(Q(tag__tag_name__icontains=tag) | 
                                                Q(content__icontains=search_item) | 
                                                Q(title__icontains=search_item) | 
                                                Q(user__nickname__icontains=search_item)) 
                queryset = queryset.order_by('-created_at').distinct()
            else: 
                queryset = queryset.filter(tag__tag_name__icontains=tag).order_by('-created_at')
        
        else:
            if search is not None:
                queryset = Post.objects.none()
                for search_item in search.split():
                    queryset = queryset | Post.objects.filter(Q(content__icontains=search_item) | 
                                                    Q(title__icontains=search_item) | 
                                                    Q(user__nickname__icontains=search_item)) 
                queryset = queryset.order_by('-created_at').distinct()
        return queryset