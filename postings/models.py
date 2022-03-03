from django.db import models
from core.models import TimeStampModel


class Category(models.Model):
    category      = models.CharField(max_length=15, unique=True)
    parent        = models.ForeignKey('self', on_delete=models.CASCADE, related_name='main_category', null = True)
    
    class Meta:
        db_table = 'categories'

    
class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)  
    
    class Meta:
        db_table = 'tags' 
            

class Post(TimeStampModel):
    title    = models.CharField(max_length=100)
    content  = models.CharField(max_length=5000)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reader   = models.IntegerField(null=True)
    tag     = models.ManyToManyField(Tag, through='TagList')
    
    class Meta:
        db_table = 'posts'   

  
class TagList(models.Model):
    tag  = models.ForeignKey('Tag', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
        

class Comment(TimeStampModel):
    content      = models.CharField(max_length=500)
    post         = models.ForeignKey('Post', on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    parent       = models.ForeignKey('self', on_delete=models.CASCADE, related_name='main_comment', null = True)
    
    class Meta:
        db_table  = 'comments'
        

class Like(models.Model):
    is_liked = models.BooleanField()
    post     = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment  = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'likes'