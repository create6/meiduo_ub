from django.db import models
from django.shortcuts import render
from django.db import models
from meiduo_mall.utils.models import BaseModel
#QQ登录
class OAuthQQUser(BaseModel):
    user=models.ForeignKey("users.User",on_delete=models.CASCADE,
                           verbose_name="关联的美多用户")

    openid=models.CharField(max_length=64,verbose_name="openid")
    class Meta:
        db_table="tb_oauth_qq"

#新浪登录
class OAuthSinaUser(BaseModel):
    """
    Sina登录用户数据
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    uid = models.CharField(max_length=64, verbose_name='access_token', db_index=True)

    class Meta:
        db_table = 'tb_oauth_sina'
        verbose_name = 'sina登录用户数据'
        verbose_name_plural = verbose_name