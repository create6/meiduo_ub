
from django.conf.urls import url
from . import views

urlpatterns=[
    # 购物车
    url(r'^carts/$', views.CartsView.as_view(), name='carts'),
    url(r'^carts/selection/$', views.SelectedAllView.as_view(), name='selected_all'),
    url(r'^carts/simple/$', views.CartSimpleView.as_view(), name='cart_simple'),
]




