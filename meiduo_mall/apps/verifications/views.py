import random
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.sms import CCP


# 图片验证
class ImageCodeView(View):
    def get(self,request,image_code_id):
        #1.
        text,image_data=captcha.generate_captcha()

        #2,save image to redis 要在settings中配置
        redis_conn=get_redis_connection("code")
        # setex分别传入的参数key,time,value
        redis_conn.setex("image_code_%s"%image_code_id,300,text)

        #3 response
        return http.HttpResponse(image_data,content_type="image/Png")

#短信验证
class SmsCodeView(View):
    def get(self,request,mobile):
        # 1 短信验证前先接收图片验证的参数进行判断。获取参数
        image_code = request.GET.get("image_code")
        image_code_id =request.GET.get("image_code_id")

        #2校验参数
        #2.1为空校验
        if not all([image_code,image_code_id]):
            return http.JsonResponse({"errmsg":"参数不全","code":10})
        #2.2 校验图片验证码正确性，要取出redis中的值
        redis_conn=get_redis_connection("code")
        #redis_image_code 是二进制参数，需要转换
        redis_image_code=redis_conn.get("image_code_%s"%image_code_id)
        #2.3 判断是否过期
        if not redis_image_code:
            return http.JsonResponse({"errmsg":"图片验证码已过期",
                                      "code":10 })
        #删除图片，防止重新验证
        redis_conn.delete("image_code_%s"%image_code_id)
        #判断图片验证码正确性,两者都转化为小写进行比较,
        if image_code.lower() != redis_image_code.lower().decode():
            return http.JsonResponse({"errmsg":"图片错误",
                                      "code":10 })
        #判断短信是否发送频繁
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            return http.JsonResponse({
                "errmsg": "频繁发送", "code": 10
            })

        # redis_conn.setex("send_flag_%s" % mobile, 0, True)

        #3 发送短信
        #3.1生成6位随机数字
        sms_code="%06d"%random.randint(0,999999)

        # ccp=CCP()
        # ccp.send_template_sms(mobile,[sms_code,5],1)
        # #保存至redis中  setex分别传入的参数key,time,value
        # redis_conn.setex("sms_code_%s"%mobile,60,sms_code)


        #[2]使用celery发送短信
        from celery_tasks.send_message.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code,5)
        print("sms_code=%s!!!"%sms_code)


        # 4 pipeline 通过减少客户端与Redis的通信次数来实现降低往返延时时间
        # 保存至redis中
        pipeline=redis_conn.pipeline()#保存
        pipeline.setex("sms_code_%s"%mobile,300,sms_code)
        pipeline.setex("send_flag_%s"%mobile,60,1)
        pipeline.execute()  #提交

        #返回响应
        return http.JsonResponse({"errmsg":"发送成功","code":10})