from decimal import Decimal
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView

#订单页面视图
class OrderSettlementView(MyLoginRequiredMiXinView):

    def get(self,request):
        #1 获取地址信息
        try:
            addresses=request.user.addresses.filter(is_deleted=False).all()
        except Exception as e:
            #未添加地址
            addresses=None

        #2查询用户所有的勾选商品
        user=request.user
        redis_conn=get_redis_connection("cart")
        cart_dict=redis_conn.hgetall("cart_%s"%user.id)
        cart_selected_list=redis_conn.smembers("cart_selected_%s"%user.id)

        #3将商品编号转换成商品数据
        sku_list=[]
        #定义总数量及总金额变量
        total_count=0
        total_amount=0
        for sku_id in cart_selected_list:
            from goods.models import SKU
            sku=SKU.objects.get(id=sku_id)
            c_count=int(cart_dict[sku_id])
            c_amount=sku.price*c_count
            sku_dict={
                "id":sku.id,
                "default_image_url":sku.default_image_url.url,
                "name":sku.name,
                "price":sku.price,
                "count":c_count,
                "amount":c_amount
            }
            sku_list.append(sku_dict)
            #累加
            total_count +=c_count
            total_amount +=c_amount
        #3.2运费与实付款
        freight=Decimal(10.0)  #Decimal为精确小数，不使用float
        finally_sum=total_amount - freight


        #4拼接数据，返回响应..(传参)
        context={
            "addresses":addresses,
            "skus":sku_list,
            "freight":freight,
            "finally_sum":finally_sum,
            "total_count":total_count,
            "total_amount":total_amount

        }




        return render(request, "place_order.html",context=context)

#
class OrderCommitView(MyLoginRequiredMiXinView):
    def post(self,request):
        #1获取参数

        #2校验参数

        #3数据入库


        pass





