from django.conf.urls import url
from . import views

urlpatterns=[
    #订单页面
    url(r'^orders/settlement/$',views.OrderSettlementView.as_view()),
    #提交订单
    url(r'^orders/commit/$',views.OrderCommitView.as_view()),
    #成功提交后，支付页面
    url(r'^orders/success/$',views.OrderSuccessView.as_view()),
    #用户订单展示
    url(r'^orders/info/(?P<page_num>\d+)/$',views.UserOrderInfoView.as_view()),
    #评价页面在/orders/comment/?order_id=' + order_id;
    url(r'^orders/comment/$',views.OrderCommentView.as_view()),
    #给评价页面传参   orders/'+this.order_id+'/uncommentgoods/
    url(r'^orders/(?P<order_id>\d+)/uncommentgoods/$',views.CommentGoodsView.as_view()),
    #orders/'+this.order_id+'/comments/
    url(r'^orders/(?P<order_id>\d+)/comments/$',views.CommentGoods2View.as_view()),

    ]