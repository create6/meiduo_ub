from django.conf.urls import url
from . import views



'''来自register.js
  // 向后端接口发送请求，让后端发送短信验证码
  var url = this.host + '/sms_codes/' + this.mobile +
  '/?image_code=' + this.image_code + '&image_code_id=' + this.image_code_id;'''



urlpatterns=[
    #   /image_codes/f7aff722-59f7-4cce-9f2d-3f9a761ee5ad/
    url(r'^image_codes/(?P<image_code_id>.+)$',views.ImageCodeView.as_view()),
#/sms_codes/18520395753/
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SmsCodeView.as_view())
]