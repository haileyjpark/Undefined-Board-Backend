from .models import Category, Post, Tag, TagList, Comment
from rest_framework import serializers
from django.db               import transaction
from django.core.exceptions  import ObjectDoesNotExist


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.get_queryset().create(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Tag
        fields       = ['tag']
        extra_kwargs = {
            'tag' : {
                'validators' : []
            }
        }

class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TagList
        fields = ['tag']
            
            
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')
    tag  = CreatableSlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='tag')
    category = serializers.CharField(source='category.category')
    
    class Meta:
        model = Post 
        fields = ['id', 'title', 'reader', 'user', 'category', 'created_at', 'content', 'tag']
        read_only_fields = ['id', 'created_at', 'reader']
        
    @transaction.atomic() 
    def create(self, validated_data):
        validated_tags = validated_data.pop('tag')
        validated_data['category'] = Category.objects.get(category=validated_data['category'])
        post = self.Meta.model.objects.create(**validated_data)
        
        for tag in validated_tags:
            obj, created = Tag.objects.get_or_create(tag=tag, defaults={'tag':tag})
            TagList.objects.get_or_create(tag=obj, post=post)

        post.save()
        return post
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at', 'content']
        read_only_fields = ['id', 'created_at', 'main_comment', 'post']
        
    def create(self, validated_data):
        validated_data['post'] = Post.objects.get(id=validated_data['post'])
        
        if 'main_comment' in validated_data:
            validated_data['main_comment'] = Comment.objects.get(parent=validated_data['main_comment'])
        
        comment = self.Meta.model.objects.create(**validated_data)

        comment.save()
        return comment
        
