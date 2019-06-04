from django.conf.urls import url
from . import views

urlpatterns=[
    #qq 第三方登录路径 ，qq前面还要加 ‘/’
    url(r'^qq/login/$',views.OAuthQQLoginView.as_view()),
    #qq 返回页面 callback
    url(r'^oauth_callback/$',views.OAuthUserView.as_view()),


]