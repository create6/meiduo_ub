from django.conf.urls import url
from . import views

urlpatterns=[
    #qq 第三方登录路径 ，qq前面还要加 ‘/’
    url(r'^qq/login/$',views.OAuthQQLoginView.as_view()),
    #qq 返回页面 callback
    url(r'^oauth_callback/$',views.OAuthUserView.as_view()),

    #sin_login
    url(r'^sina/login/$',views.SinaLoginView.as_view()),
    #sina callback   http://www.meiduo.site:8000/sina_callback?code=3fc775ee34eb5fdc1e26db7820c14a83
    url(r'^sina_callback/$',views.SinaCallBackView.as_view()),

    #/oauth/sina/user/?code=' + code
    url(r'^oauth/sina/user/$',views.SinaCallBack2View.as_view()),







]