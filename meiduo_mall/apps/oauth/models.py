from django.db import models
from django.shortcuts import render
from django.db import models
from meiduo_mall.utils.models import BaseModel

class OAuthQQUser(BaseModel):
    user=models.ForeignKey("users.User",on_delete=models.CASCADE,
                           verbose_name="关联的美多用户")

    openid=models.CharField(max_length=64,verbose_name="openid")
    class Meta:
        db_table="tb_oauth_qq"