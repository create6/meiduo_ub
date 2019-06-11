from django import http
import json
from decimal import Decimal
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from goods.models import SKU
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView
from orders.models import OrderInfo, OrderGoods
from users.models import Address
from django.utils import timezone



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
            "payment_amount":finally_sum,
            "total_count":total_count,
            "total_amount":total_amount
        }

        return render(request, "place_order.html",context=context)

#提交订单
class OrderCommitView(MyLoginRequiredMiXinView):

    #设置保存点
    @transaction.atomic
    def post(self,request):
        #1获取参数（参数后端-->js-->后端 ）
        dict_data=json.loads(request.body.decode())
        address_id=dict_data.get("address_id")
        pay_method=dict_data.get("pay_method")  #支付方式
        user=request.user

        #2校验参数
        #2.1为空校验
        if not all([address_id,pay_method]):
            return http.HttpResponseForbidden("参数不全")
        #2.2地址校验(此参数本身是后端传给前端，再从前端返回至后端，还有必要校验？答：防止中间篡改，eg爬虫，攻击）
        try:
            address=Address.objects.get(id=address_id)
        except Exception as e:
            return http.HttpResponseForbidden("地址不存在")
        #2.3支付方式校验
        pay_method = int(pay_method)
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM["CASH"],OrderInfo.PAY_METHODS_ENUM["ALIPAY"],]:
            return http.HttpResponseForbidden("支付方式有误")
        #2.4构建订单编号，时间戳
        order_id=timezone.now().strftime('%Y%m%d%H%M%S')+"%06d"%user.id
        #2.5创建支付状态
        if pay_method == OrderInfo.PAY_METHODS_ENUM["CASH"]:
            status =OrderInfo.ORDER_STATUS_ENUM["UNSEND"]
        else:
            #支付宝支付
            status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"]

        #TODO 入库前设置保存点。方便回滚
        sid = transaction.savepoint()
        #3数据入库(订单信息）表1
        order=OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,                ######
            total_amount=Decimal(0.0),    ######
            freight=Decimal(10.0),
            pay_method=pay_method,
            status=status,

        )

        #4订单商品信息入库,表2
        redis_conn=get_redis_connection("cart")
        cart_dict=redis_conn.hgetall("cart_%s"%user.id)
        cart_selected_list=redis_conn.smembers("cart_selected_%s"%user.id)
        for sku_id in cart_selected_list:
            #TODO 死循环
            while True:
                #4.1获取商品对象，数量
                sku=SKU.objects.get(id=sku_id)
                count=int(cart_dict[sku_id])
                #4.2判断库存是否足够
                if count >sku.stock:

                    # TODO 库存不足时回滚，不保存数据
                    transaction.savepoint_rollback(sid)
                    return http.HttpResponseForbidden("库存不足")

                # #4.3 商品信息：减少库存参数及增加销量参数,保存参数
                # sku.stock -=count
                # sku.sales +=count
                # sku.save()

                #TODO 乐观锁解决并发下单问题
                #数据准备
                old_stock=sku.stock
                old_sales=sku.sales

                new_stock=old_stock -count
                new_sales=old_sales +count
                #update方法返回的整数，表示影响的行数
                ret=SKU.objects.filter(id=sku_id,stock=old_stock).update(stock=new_stock,sales=new_sales)
                if ret ==0:
                    # transaction.savepoint_rollback(sid)#TODO 回滚
                    # return http.HttpResponseForbidden("系统繁忙！！！")
                    continue #重新循环

                #4.4设置order信息，累加
                order.total_count +=count
                order.total_amount +=(count * sku.price)

                #4.5创建订单商品信息对象 ,不需要实例化
                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=sku.price,
                )
                break #跳出

        #5提交订单
        order.save()
        #TODO 事务提交
        transaction.savepoint_commit(sid)

        #6清空redis中选中的商品
        redis_conn.hdel("cart_%s"%user.id,*cart_selected_list)
        redis_conn.srem("cart_selected_%s"%user.id,*cart_selected_list)

        #7返回响应
        context={
            "code":0,
            "order_id":order_id,
            "payment_amount":order.total_amount+order.freight,
            "pay_method":pay_method,
        }

        return http.JsonResponse(context)

#支付页面
class OrderSuccessView(MyLoginRequiredMiXinView):
    def get(self,request):
        #1获取参数,地址栏中
        # #/?order_id=20190610012757000001&payment_amount=3778&pay_method=1
        order_id=request.GET.get("order_id")
        payment_amount=request.GET.get("payment_amount")
        pay_method=request.GET.get("pay_method")
        # #2校验参数,与数据库比较
        # if not all([order_id,payment_amount,pay_method]):
        #     return http.HttpResponseForbidden("参数不全")
        #

        #2拼接数据，渲染页面
        context={
            "order_id":order_id,
            "pay_method":pay_method,
            "payment_amount":payment_amount,
        }
        return render(request,'order_success.html',context=context)

#订单展示
class UserOrderInfoView(MyLoginRequiredMiXinView):
    def get(self,request,page_num):
        #1查询用户订单
        # OrderInfo.objects.filter(user_id=request.user.id)
        orders=request.user.orders.order_by("-create_time")

        #1.1处理支付方式和状态（订单中心查看订单状态）
        for order in orders:
            order.paymethod_name=OrderInfo.PAY_METHOD_CHOICES[order.pay_method-1][1]
            order.status_name=OrderInfo.ORDER_STATUS_CHOICES[order.status-1][1]

        #2分页
        paginate=Paginator(object_list=orders,per_page=4)
        page=paginate.page(page_num)
        orders_list=page.object_list#当前页对象列表
        current_page=page.number#当前页
        total_page=paginate.num_pages#总页数

        #3传参，渲染
        context={
            "orders":orders_list,
            "current_page":current_page,
            "total_page":total_page
        }

        return render(request,"user_center_order.html",context=context)




