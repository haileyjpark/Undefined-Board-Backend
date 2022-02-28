from django.db import models

from core.models     import TimeStampModel

class User(TimeStampModel):
    name                = models.CharField(max_length=50)
    phone_number        = models.CharField(max_length=50,null=True)
    profile_image       = models.URLField(max_length=300,null=True)
    description         = models.CharField(max_length=1000,null=True)
    kakao_id            = models.IntegerField(unique=True)
    email               = models.CharField(max_length=200,null=True)

    class Meta:
        db_table        = 'users'