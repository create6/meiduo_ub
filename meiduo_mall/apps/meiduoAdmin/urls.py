from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns=[
        #---------------首页部分
        #登录
        url(r'^authorizations/$',obtain_jwt_token),
        url(r'^statistical/total_count/$',views.UserTotalCountView.as_view()),
        url(r'^statistical/day_increment/$',views.UserDayIncrementView.as_view()),
        url(r'^statistical/day_active/$',views.UserDayActiveView.as_view()),
        url(r'^statistical/day_orders/$',views.UserDayOrdersView.as_view()),
        url(r'^statistical/goods_day_views/$',views.UserGoodsDayView.as_view()),

        #---------------用户部分
        url(r'^users/$',views.UserView.as_view()),
        #---------------商品部分
        url(r'skus/categories/$',views.SKUCategoryView.as_view({"get":"list"})),
        url(r'^goods/simple/$',views.GoodSimpleView.as_view()),


        ]


#---------------商品部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'skus',views.SKUView,base_name="skus")
#3,添加路由到urlpatterns
urlpatterns += router.urls