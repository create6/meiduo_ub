from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


class MyAuthenticateBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #1判断username是否是手机号
            if re.match(r'^1[3-9]\d{9}$',username):
                #用手机查询用户信息
                user=User.objects.get(mobile=username)
            else:
                #2通过用户名查询
                user=User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            return user


