"""meiduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('users.urls',namespace='user')),
    # contents
    url(r'^', include('contents.urls', namespace='contents')),
    #add verifications  验证路由
    url(r'^',include('verifications.urls',namespace="verifications")),
    #qq_login
    url(r'^', include('oauth.urls', namespace='qqlogin')),
    #areas
    url(r'^', include('areas.urls', namespace='areas')),
    #goods
    url(r'^', include('goods.urls', namespace='goods')),

    #search
    url(r'^search/', include('haystack.urls')),
    #购物车
    url(r'^', include('carts.urls', namespace='carts')),
    #订单
    url(r'^', include('orders.urls', namespace='orders')),
    #支付
    url(r'^', include('payment.urls', namespace='payment')),


]
