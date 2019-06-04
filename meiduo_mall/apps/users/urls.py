# 编写子应用的urls
from django.conf.urls import url
from . import views

urlpatterns=[
    #regiseter
    url(r'^register/$',views.RegisterView.as_view(),name='"register'),
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.CheckUsernameView.as_view(),name="username"),
    url(r'^mobiles/(?P<mobile>1[3456789]\d{9})/count/$',views.CheckMobileView.as_view(),name='mobile'),
    #login
    url(r'^login/$',views.LoginView.as_view(),name='"login'),
    #logout
    url(r'^logout/$',views.LogoutView.as_view(),name='"logout'),
    #info 用户中心
    url(r'^info/$',views.UserCenter.as_view(),name='info'),
    # 用户中心添加邮箱
    url(r'^emails/$', views.SendEmail.as_view(), name='emails'),
    #激活邮箱
    url(r'^emails/verification/$', views.EmailActiveView.as_view(), name='email_verify'),
    #address
    url(r'^addresses/$',views.AddressView.as_view(),name='look_add'),
    # add new address
    url(r'^addresses/create/$',views.NewAddressView.as_view(),name='new_address'),
    #set default address
    url(r'^addresses/(?P<defaultAdd>\d+)/default/$',views.SetDefaultAddView.as_view(),name='look_add'),
    #modify address  #delete address addresses/1/
    url(r'^addresses/(?P<address_id>\d+)/$',views.UpdateADDView.as_view(),name='address_id'),
    #modify address-title
    url(r'^addresses/(?P<address_id>\d+)/title/$',views.AddressTitleView.as_view(),name='address_title'),
    #modify password
    url(r'^password/$',views.ModifyPassWordView.as_view(),name='modify_password'),




    ]
