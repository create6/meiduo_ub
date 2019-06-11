from django import http
from django.shortcuts import render

from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView
from alipay import AliPay
from django.conf import settings #导入设置
from orders.models import OrderInfo
from payment.models import Payment
#支付页面
class PayView(MyLoginRequiredMiXinView):
    def get(self,request,order_id):

        #0取出订单对象
        try:
            order=OrderInfo.objects.get(order_id=order_id)
        except Exception as e:
            return http.HttpResponseForbidden("非法请求")

        #1密钥
        app_private_key_string = open(settings.APLIPAY_PRIVATE_KEY).read()
        alipay_public_key_string = open(settings.APLIPAY_PUBLIC_KEY).read()

        #2创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = False  # 默认False
        )
        #3生成订单字符串
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount+order.freight),
            subject="美多商城订单",
            return_url=settings.ALIPAY_RETURN_URL,
            # notify_url=settings.ALIPAY_URL  # 可选, 不填则使用默认notify url
        )
        #4生成跳转url
        alipay_url=settings.ALIPAY_URL+ order_string

        return http.JsonResponse({"code":0,"alipay_url":alipay_url})

#回调页面
class PaymentStatusView(MyLoginRequiredMiXinView):
    def get(self,request):
        #1获取参数
        dict_data=request.GET.dict()
        sign=dict_data.pop("sign")

        #2校验参数
        app_private_key_string = open(settings.APLIPAY_PRIVATE_KEY).read()
        alipay_public_key_string = open(settings.APLIPAY_PUBLIC_KEY).read()

        #3创建alipay对象
        alipay=AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = False  # 默认False
        )
        #验证正确性
        success=alipay.verify(dict_data,sign)
        if not success:
            return http.HttpResponseForbidden("非法请求")
        #4数据入库
        order_id=dict_data.get("out_trade_no")
        trade_id=dict_data.get("trade_no")
        Payment.objects.create(
            order_id=order_id,
            trade_id=trade_id
        )
        #修改订单状态
        OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT'])

        #返回响应
        return render(request,'pay_success.html',context={"trade_id":trade_id})


