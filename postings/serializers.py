from .models import Category, Post, Tag, TagList, Comment
from rest_framework import serializers
from django.db               import transaction


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
            
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at', 'content', 'post', 'parent']
        read_only_fields = ['id', 'created_at']
           
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')
    tag  = CreatableSlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='tag_name')
    category = serializers.IntegerField(source='category.id')
    comment_set = CommentSerializer(many=True, read_only=True)
        
    class Meta:
        model = Post 
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'reader']
        depth = 1
        
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
    

        
