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
    #浏览记录，路径来自detail.js请求:var url = this.hots + '/browse_histories/'
    url(r'^browse_histories/$',views.BrowseHistoryView.as_view(),name='modify_password'),
    #进入忘记密码页面
    url(r'^forgot_pwd/$',views.ForgotPwdView.as_view(),name='forgot_password'),

    # accounts/' + this.username + '/sms/token/?text='+ this.image_code + '&image_code_id=' + this.image_code_id, {
    #页面1
    url(r'^accounts/(?P<username>\w{5,20})/sms/token/$',views.ForgotPwd1View.as_view()),
    #页面2   /sms_codes/?mobile=13059185800
    url(r'^sms_codes/$',views.ForgotPwd2View.as_view()),
    #页面2.2   accounts/bo009/password/token/?sms_code=295090
    url(r'^accounts/(?P<username>\w{5,20})/password/token/$',views.ForgotPwd22View.as_view()),
    #页面3 POST /users/1/password/
    url(r'^users/(?P<user_id>\d+)/password/$',views.ForgotPwd3View.as_view()),






    ]
