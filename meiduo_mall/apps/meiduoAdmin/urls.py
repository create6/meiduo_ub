from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from meiduoAdmin.views import home_vies,sku_views,spu_views,user_views




urlpatterns=[
        #---------------首页部分
        #登录
        url(r'^authorizations/$',obtain_jwt_token),
        url(r'^statistical/total_count/$',home_vies.UserTotalCountView.as_view()),
        url(r'^statistical/day_increment/$',home_vies.UserDayIncrementView.as_view()),
        url(r'^statistical/day_active/$',home_vies.UserDayActiveView.as_view()),
        url(r'^statistical/day_orders/$',home_vies.UserDayOrdersView.as_view()),
        url(r'^statistical/goods_day_views/$',home_vies.UserGoodsDayView.as_view()),

        #---------------用户部分
        url(r'^users/$',user_views.UserView.as_view()),
        #---------------商品部分
        url(r'skus/categories/$',sku_views.SKUCategoryView.as_view()),

        #---------------
        url(r'^goods/(?P<pk>\d+)/specs/$',sku_views.SPUSpecsView.as_view()),

        ]


#---------------商品部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'skus',sku_views.SKUView,base_name="skus")
#3,添加路由到urlpatterns
urlpatterns += router.urls