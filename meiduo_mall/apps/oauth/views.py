import re
from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ
from oauth.models import OAuthQQUser, OAuthSinaUser
from oauth.utils import generate_sign_openid,decode_sign_openid
from django_redis import get_redis_connection
from carts.utils import merge_cookie_redis_cart#合并购物车
from users.models import User
from oauth.sinaweibopy3 import APIClient



class OAuthQQLoginView(View):
    def get(self,request):
        #1,获取参数
        state = request.GET.get("next","/")
        #2.创建OAuthQQ对象
        oauth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                client_secret=settings.QQ_CLIENT_SECRET,
                redirect_uri=settings.QQ_REDIRECT_URI,
                state=next)

        #获取qq登陆页面
        login_url=oauth_qq.get_qq_url()
        #返回
        return http.JsonResponse({"login_url":login_url})

class OAuthUserView(View):
    def get(self, request):
        #http://www.meiduo.site:8000/oauth_callback?code=FDE1DC283B08B2
        # 96DC530EA7DEFBDB2C&state=%3Cbuilt-in%2Bfunction%2Bnext%3E
        #1 获取url中参数code
        code =request.GET.get("code")
        state = request.GET.get("state")
        if not code:
            return http.HttpResponseForbidden("code丢失")

        #2通过code换取access_token
        oauth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                           client_secret=settings.QQ_CLIENT_SECRET,
                           redirect_uri=settings.QQ_REDIRECT_URI,
                           state=next)
        access_token=oauth_qq.get_access_token(code)
        #3通过access_token找到openid
        openid=oauth_qq.get_open_id(access_token)
        #4根据openid，取到qq用户对象,查询数据库
        try:
            oauth_qq_user=OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            #初次授权，需要配合表单提交，传参，验证
            #调用utils文件中的加密方法
            sign_openid=generate_sign_openid(openid)
            #下面的"token"是oauth_callback.html中的参数名称,openid存入url中
            return render(request, 'oauth_callback.html',context={"token":sign_openid})
        else:
            #5，非初次授权,直接登录成功
            user=oauth_qq_user.user
            #5.1 状态保持
            login(request,user)
            request.session.set_expiry(3600*24*2)
            response=redirect("/")
            response.set_cookie("username",user.username)
            # 合并购物车
            response = merge_cookie_redis_cart(request, user, response)
            #返回响应
            return response

    #处理初次授权用户表单提交
    def post(self,request):
        #1,获取参数,参数来自oauth_callback.html
        sign_openid =request.POST.get("access_token")
        mobile =request.POST.get("mobile")
        pwd =request.POST.get("pwd")
        sms_code =request.POST.get("sms_code")

        #2,校验参数
        #2.1为空校验
        if not all([sign_openid,mobile,pwd,sms_code]):
            return http.HttpResponseForbidden("参数不全")

        #2.2校验openid
        # #对openid进行解密
        openid=decode_sign_openid(sign_openid)
        if not openid:
            return http.HttpResponseForbidden("openid过期")

        #2.3校验手机号的格式
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return http.HttpResponseForbidden("手机号格式有误")

        #2.4校验密码的格式
        if not re.match(r'^[0-9a-zA-Z]{8,20}$',pwd):
            return http.HttpResponseForbidden("密码格式有误")
        #2.5校验短信验证码的正确性
        #连接redis
        redis_conn=get_redis_connection("code")
        #查询存在redis中的短信验证码
        redis_sms_code=redis_conn.get("sms_code_%s"%mobile)
        #判断是否过期
        if not redis_sms_code:
            return http.HttpResponseForbidden("短信验证码已过期")
        #判断正确性,redis_sms_code 为二进制类型，应转换
        if redis_sms_code.decode() != sms_code:
            return http.HttpResponseForbidden("短信验证码错误")

        #3,判断是否存在美多用户，在tb_user里匹配
        try:
            user=User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            #3.1 手机号不存在，为其创建美多账号
            user=User.objects.create_user(username=mobile,password=pwd,
                                          mobile=mobile)
            #3.2绑定美多用户 qq用户
            OAuthQQUser.objects.create(openid=openid,user=user)

            # 3.3密码正确，状态保持
            login(request, user)
            request.session.set_expiry(3600 * 24 * 2)
            # 3.4返回首页
            response = redirect("/")
            response.set_cookie("username", user.username, max_age=3600 * 24 * 2)
            # 合并购物车
            response = merge_cookie_redis_cart(request, user, response)
            return response

        else:
            #3.2 手机号存在，直接绑定
            #4校验密码正确性
            if not user.check_password(pwd):
                return http.HttpResponseForbidden("密码错误")
            #4.1密码正确，状态保持
            login(request,user)
            request.session.set_expiry(3600*24*2)
            #4.2返回首页
            response=redirect("/")
            response.set_cookie("username",user.username,max_age=3600*24*2)
            # 合并购物车
            response = merge_cookie_redis_cart(request, user, response)
            return response


#sina login
class SinaLoginView(View):
    def get(self,request):
        #1,获取参数
        state = request.GET.get("next","/")
        #2.创建OAuthQQ对象

        oauth_sina = APIClient(app_key=settings.APP_KEY,
                               app_secret=settings.APP_SECRET,
                               redirect_uri=settings.REDIRECT_URL,

                               )

        #获取sina登陆页面
        login_url=oauth_sina.get_authorize_url()
        #返回
        return http.JsonResponse({"login_url":login_url})

#sina callback   根据前端需求，此接口仅需响应页面，不需要其他参数
class SinaCallBackView(View):
    def get(self,request):
        #1获取参数
        return render(request,"sina_callback.html")


#此请求由sina_callback.html   加载的js文件发出的请求
#  axios.get(this.host + '/oauth/sina/user/?code=' + code, {responseType: 'json',
class SinaCallBack2View(View):
    def get(self,request):
        #获取参数
        code=request.GET.get("code")
        if not code:
            return http.HttpResponseForbidden("code丢失")
        #对象
        oauth_sina = APIClient(app_key=settings.APP_KEY,
                               app_secret=settings.APP_SECRET,
                               redirect_uri=settings.REDIRECT_URL,

                               )

        result=oauth_sina.request_access_token(code)
        access_token=result.access_token
        uid=result.uid

        # 4根据uid，取到sina用户对象,查询数据库
        try:
            oauth_sina_user = OAuthSinaUser.objects.get(uid=uid)
        except OAuthSinaUser.DoesNotExist:
            # 初次授权
            # 调用utils文件中的加密方法
            sign_uid = generate_sign_openid(uid)
            #TODO 下面的"access_token"是传递给js使用 ??
            return http.JsonResponse({"access_token": sign_uid})

        else:
            # 5，非初次授权
            user = oauth_sina_user.user
            # 5.1 状态保持
            login(request, user)
            request.session.set_expiry(3600 * 24 * 2)
            response = redirect("/")
            response.set_cookie("username", user.username)
            # 合并购物车
            response = merge_cookie_redis_cart(request, user, response)
            # 返回响应
            return response



