from .models import Category, Post, PostLike, Tag, TagList, Comment, CommentLike
from users.models import User
from rest_framework import serializers
from django.db import transaction


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Tag
        fields       = ['tag_name']
        extra_kwargs = {
            'tag_name' : {
                'validators' : []
            }
        }


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TagList
        fields = ['tag']
  
  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 
        
            
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(method_name='get_like_count')
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at', 'content', 'post', 'parent', 'like_count']
        read_only_fields = ['id', 'created_at', 'user', 'like_count']
        
    def get_like_count(self, obj):
        like_count = CommentLike.objects.filter(comment=obj).count()
        return like_count
        
           
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tag  = CreatableSlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='tag_name')
    category = serializers.IntegerField(source='category.id')
    comment_set = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField(method_name='get_like_count')
    
    class Meta:
        model = Post 
        fields = ['title', 'content', 'category', 'user', 'viewer', 
                  'tag', 'created_at', 'like_count', 'comment_set']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reader',
                            'like_count']
        depth = 1
        
    def get_like_count(self, obj):
        like_count = PostLike.objects.filter(post=obj).count()
        return like_count
    
    @transaction.atomic() 
    def create(self, validated_data):
        validated_tags = validated_data.pop('tag')
        validated_data['category'] = Category.objects.get(id=validated_data['category']['id'])
        post = self.Meta.model.objects.create(**validated_data)
        
        for tag in validated_tags:
            obj, created = Tag.objects.get_or_create(tag_name=tag.tag_name, defaults={'tag_name':tag.tag_name})
            TagList.objects.get_or_create(tag=obj, post=post)

        post.save()
        return post
    
    
class PostLikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostLike
        fields = '__all__'
        

class CommentLikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommentLike
        fields = '__all__'
