from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from meiduoAdmin.views import home_views,sku_views,spu_views,user_views
from meiduoAdmin.views import spu_specsOptionViews
from meiduoAdmin.views import spu_specs_views

urlpatterns=[
        #---------------首页部分
        #登录
        url(r'^authorizations/$',obtain_jwt_token),
        url(r'^statistical/total_count/$',home_views.UserTotalCountView.as_view()),
        url(r'^statistical/day_increment/$',home_views.UserDayIncrementView.as_view()),
        url(r'^statistical/day_active/$',home_views.UserDayActiveView.as_view()),
        url(r'^statistical/day_orders/$',home_views.UserDayOrdersView.as_view()),
        url(r'^statistical/goods_day_views/$',home_views.UserGoodsDayView.as_view()),

        #---------------用户部分
        url(r'^users/$',user_views.UserView.as_view()),
        #---------------商品部分
        url(r'skus/categories/$',sku_views.SKUCategoryView.as_view()),
        url(r'^goods/(?P<pk>\d+)/specs/$',sku_views.SPUSpecsView.as_view()),
#---------------spu
        url(r'^goods/brand/simple/$',spu_views.SPUView.as_view({"get":"brand"})),
        url(r'^goods/channel/categories/$',spu_views.SPUView.as_view({"get":"category"})),
        url(r'^goods/channel/categories/(?P<pk>\d+)/$',spu_views.SPUView.as_view({"get":"category_sub"})),
        #上传图片
        url(r'^goods/images/$',spu_views.SPUView.as_view({"post":"upload_image"})),
#
        url(r'^goods/specs/simple/$',spu_specsOptionViews.SpuSpecsView.as_view()),



        ]





#---------------spu_specs_option部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'specs/options',spu_specsOptionViews.SpuSpecOptionView,base_name="specOptions")
#3,添加路由到urlpatterns
urlpatterns += router.urls
#---------------spu_specs部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'goods/specs',spu_specs_views.SpuSpecView,base_name="spes")
#3,添加路由到urlpatterns
urlpatterns += router.urls
#---------------spu部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'goods',spu_views.SPUView,base_name="spus")
#3,添加路由到urlpatterns
urlpatterns += router.urls
#---------------sku部分
#1,创建路由
router = DefaultRouter()
#2,注册视图集
router.register(r'skus',sku_views.SKUView,base_name="skus")
#3,添加路由到urlpatterns
urlpatterns += router.urls