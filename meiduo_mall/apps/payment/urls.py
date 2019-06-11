from django.conf.urls import url
from . import views

urlpatterns=[
    #订单页面
    url(r'^payment/(?P<order_id>\d+)/$',views.PayView.as_view()),
    #支付成功后回调页面
    url(r'^payment/status/$',views.PaymentStatusView.as_view()),

]





