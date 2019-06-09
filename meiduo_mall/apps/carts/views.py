import json
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from goods.models import SKU
import base64
import pickle

#购物车视图
class CartsView(View):
    #添加购物车
    def post(self,request):
        #1 获取参数
        dict_data=json.loads(request.body.decode())
        sku_id=dict_data.get("sku_id")
        count=dict_data.get("count")
        selected=dict_data.get("selected",True)
        user=request.user
        #2 校验参数
        #2.1为空校验
        if not all([sku_id,count]):
            return http.HttpResponseForbidden("参数不全")
        #2.2判断count是否是整数
        try:
            count=int(count)
        except Exception as e:
            return http.HttpResponseForbidden("购买数量错误")
        #2.3校验商品对象是否存在
        try:
            sku=SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不存在")
         #2.4校验库存是否充足
        if count > sku.stock:
            return http.HttpResponseForbidden("库存不足")
        #3 判断用户登录状态
        if user.is_authenticated:
            #登录状态（登录的用户）,读取redis里面的数据
            #3.1 获取redis对象
            redis_conn =get_redis_connection("cart")
            #3.2添加数据到redis,hincrby:有则增加，无则新增
            redis_conn.hincrby("cart_%s"%user.id,sku_id,count)
            if selected:
                redis_conn.sadd("cart_selected_%s"%user.id,sku_id)
            #3.3返回响应
            return  http.JsonResponse({"code":0})
        else:
            #非登录状态，读取cookie里面的数据
            #4.1读取数据
            cookie_cart = request.COOKIES.get("cart")
            #4.2转为字典
            cookie_dict = {}
            #判断是否存在
            if cookie_cart:
                #解密cookie
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))
            #4.3累加count
            if sku_id in cookie_dict:
                count +=cookie_dict[sku_id].get("count")
            #4.4设置新数据：
            cookie_dict[sku_id]={
            "count":count,
            "selected":selected
            }
            #4.5设置cookie，返回响应
            response=http.JsonResponse({"code":0})
            cookie_cart=base64.b64encode(pickle.dumps(cookie_dict)).decode()
            response.set_cookie("cart",cookie_cart)
            return response
    #展示购物车页面
    def get(self,request):
        #1,判断用户登录状态
        user=request.user
        if user.is_authenticated:
            #登录状态
            #1.获取redis数据
            redis_conn =get_redis_connection("cart")
            cart_dict=redis_conn.hgetall("cart_%s"%user.id)
            cart_selected_list=redis_conn.smembers("cart_selected_%s"%user.id)
            #2拼接数据
            sku_list=[]
            for sku_id,count in cart_dict.items():
                sku=SKU.objects.get(id=sku_id)
                sku_dict={
                  "default_image_url":sku.default_image_url.url,
                    "name":sku.name,
                    "price":str(sku.price),
                    #小计，注意数据类型
                    "amount":str(int(count)*sku.price),
                    "selected":str(sku_id in cart_selected_list),
                    "count":int(count),
                    "id":sku.id #后面需要用到
                }
                sku_list.append(sku_dict)
            context={
                "sku_carts":sku_list
            }
            return render(request, "cart.html", context)
        else:
            #非登录状态
            #1.获取参数，cookie
            cookie_cart=request.COOKIES.get("cart")
            #2判断购物车cookie是否存在
            if not cookie_cart:
                return render(request,'cart.html')   #此页面应为cart.html
            # try:
            #     cookie_cart = request.COOKIES.get("cart")
            # except Exception as e:
            #     return render(request, 'detail.html')
            #有cookie数据
            #3数据转换
            cookie_dict=pickle.loads(base64.b64decode(cookie_cart.encode()))

            sku_list=[]
            for sku_id,count_selected in cookie_dict.items():
                sku=SKU.objects.get(id=sku_id)
                sku_dict={
                    "default_image_url":sku.default_image_url.url,
                    "name":sku.name,
                    "price":str(sku.price),
                    "amount":str(sku.price*int(count_selected["count"])),
                    "count":int(count_selected["count"]),
                    "selected": str(count_selected["selected"]),
                    "id":sku.id

                }
                sku_list.append(sku_dict)
            #4响应#看前端需要什么数据就返回什么数据
            context={
                "sku_carts":sku_list
            }
            return render(request,'cart.html',context=context)

    #编辑购物车，加减商品数量
    def put(self,request):
        #1获取参数
        dict_data =json.loads(request.body.decode())
        sku_id =dict_data.get("sku_id")
        count=dict_data.get("count")
        selected =dict_data.get("selected",True)

        #2校验参数
        #2.1为空校验
        if not all([sku_id,count]):
            return http.HttpResponseForbidden("参数不全")

        #2.2判断sku_id对象是否存在
        try:
            sku=SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不存在")

        #2.3将count整数化
        try:
            cont=int(count)
        except Exception as e:
            return http.HttpResponseForbidden('count数量有误')

        #3判断用户状态
        user=request.user
        if user.is_authenticated:
            #用户存在
            #3.1获取redis对象
            redis_conn=get_redis_connection("cart")
            #3.2修改数据
            redis_conn.hset("cart_%s"%user.id,sku_id,count)
            #是否选中
            if selected:
                #选中
                redis_conn.sadd("cart_selected_%s"%user.id,sku_id)
            else:
                #不选中
                redis_conn.srem("cart_selected_%s"%user.id,sku_id)
            #3.3拼接数据返回响应 #针对 cart.js中update_count 所需参数
            context={
                "code":'0',
                "cart_sku":{
                     "default_image_url":sku.default_image_url.url,
                    "name":sku.name,
                    "price":str(sku.price),
                    #小计，注意数据类型
                    "amount":str(int(count)*sku.price),
                    "selected":str(selected),
                    "count":int(count),
                    "id":sku.id
                }


            }
            #返回
            return http.JsonResponse(context)

        # 用户不存在
        else:
            #4.1获取cookie中的数据
            cookie_cart=request.COOKIES.get("cart")
            #4.2 str 转字典
            cookie_dict={}
            #判断是否有cookie数据
            if cookie_cart:
                #str转字典
                cookie_dict=pickle.loads(base64.b64decode(cookie_cart.encode()))
            #4.3修改参数
            cookie_dict[sku_id]={
                "count":count,
                "selected":selected
            }
            context = {
                "code":0,
                "cart_sku":{
                    "default_image_url": sku.default_image_url.url,
                    "name": sku.name,
                    "price": str(sku.price),
                    # 小计，注意数据类型
                    "amount": str(int(count) * sku.price),
                    "selected": selected,#非登录状态下的selected数据类型不用转换，原因：前端已经转换。而登录状态下前端未转换
                    "count": int(count),
                    "id": sku.id
                }

            }
            response=http.JsonResponse(context)
            # 4.4 字典转str
            cookie_cart=base64.b64encode(pickle.dumps(cookie_dict)).decode()
            #存储cookie
            response.set_cookie("cart",cookie_cart)
            #返回
            return response

    #删除购物车中的商品
    def delete(self,request):
        #1获取参数
        dict_data =json.loads(request.body.decode())
        sku_id =dict_data.get("sku_id")
        #2校验参数
        #2.1为空校验
        if not sku_id:
            return http.HttpResponseForbidden("参数不全")
        #2.2判断sku_id对象是否存在
        try:
            sku=SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不存在")
        #3判断用户状态
        user=request.user
        if user.is_authenticated:
            #用户存在
            #3.1获取redis对象
            redis_conn=get_redis_connection("cart")
            #加入管道
            pipeline=redis_conn.pipeline()
            #3.2删除数据
            pipeline.hdel("cart_%s"%user.id,sku_id)
            pipeline.srem("cart_selected_%s"%user.id,sku_id)
            #管道提交
            pipeline.execute()

            #返回
            return http.JsonResponse({"code":0,"errmsg":"success"})

        # 用户不存在
        else:
            #4.1获取cookie中的数据
            cookie_cart=request.COOKIES.get("cart")
            #4.2 str 转字典
            cookie_dict={}
            #判断是否有cookie数据
            if cookie_cart:
                #str转字典
                cookie_dict=pickle.loads(base64.b64decode(cookie_cart.encode()))
            #4.3删除数据,删除字典的方法
            if sku_id in cookie_dict:
                del cookie_dict[sku_id]
            #返回响应
            response=http.JsonResponse({"code":0,"errmsg":"success"})
            # 4.4 字典转str
            cookie_cart=base64.b64encode(pickle.dumps(cookie_dict)).decode()
            #存储cookie
            response.set_cookie("cart",cookie_cart)
            #返回
            return response

#全不选与全选功能
class SelectedAllView(View):
    def put(self,request):
        #1 获取参数,全选与否
        selected=json.loads(request.body.decode()).get("selected",True)  #注意此处的括号
        #2 判断用户状态
        user=request.user
        if user.is_authenticated:
            #已登录
            #2.1获取redid对象，获取数据
            redis_conn=get_redis_connection("cart")
            cart_dict=redis_conn.hgetall("cart_%s"%user.id)
            sku_id_list=cart_dict.keys()
            #2.2全选与否
            if selected:
                #全选
                redis_conn.sadd("cart_selected_%s"%user.id,*sku_id_list)
            else:
                #全不选
                redis_conn.srem("cart_selected_%s"%user.id,*sku_id_list)
            #2.3返回响应
            return http.JsonResponse({"code":0,"errmsg":"success"})

        else:
            #未登录
            #4.1获取cookie中的数据
            cookie_cart=request.COOKIES.get("cart")
            #4.2 str 转字典
            cookie_dict={}
            #判断是否有cookie数据
            if cookie_cart:
                #str转字典
                cookie_dict=pickle.loads(base64.b64decode(cookie_cart.encode()))
            #4.3是否是全选状态
            #遍历字典

                # cookie_dict的样式
                # {
                #     sku_id1:{
                #     "count": count,
                #     "selected": selected
                # },
                #     sku_id2: {
                #         "count": count,
                #         "selected": selected
                #
                # }
            for sku_id in cookie_dict:
                cookie_dict[sku_id]["selected"]=selected

            #返回响应
            response=http.JsonResponse({"code":0,"errmsg":"success"})
            # 4.4 字典转str
            cookie_cart=base64.b64encode(pickle.dumps(cookie_dict)).decode()
            #存储cookie
            response.set_cookie("cart",cookie_cart)
            #返回
            return response

#首页购物车简略图
class CartSimpleView(View):
    def get(self,request):
        #1判断用户登录状态
        user=request.user
        if user.is_authenticated:
            #2 登录用户
            #2.1获取redis对象，取出数据
            redis_conn=get_redis_connection("cart")
            cart_dict=redis_conn.hgetall("cart_%s"%user.id)
            #2.2拼接数据
            sku_list=[]
            for sku_id,count in cart_dict.items():
                sku=SKU.objects.get(id=sku_id)
                sku_dict={
                    "id":sku.id,
                    "name":sku.name,
                    "default_image_url":sku.default_image_url.url,
                    "count":int(count)

                }
                sku_list.append(sku_dict)
            #返回响应
            context={
                "cart_skus":sku_list
            }
            return http.JsonResponse(context)
        else:
            #3 非登录用户
            #3.1获取cookie数据
            cookie_cart = request.COOKIES.get("cart")
            # 3.2 str 转字典
            cookie_dict = {}
            # 判断是否有cookie数据
            if cookie_cart:
                # str转字典
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))
            #3.3拼接数据
            sku_list=[]
            for sku_id,count_selected in cookie_dict.items():
                sku=SKU.objects.get(id=sku_id)
                sku_dict={
                    "id":sku.id,
                    "name":sku.name,
                    "default_image_url":sku.default_image_url.url,
                    "count":int(count_selected["count"])
                }
                sku_list.append(sku_dict)
            #4返回响应
            context = {
                "cart_skus": sku_list
            }
            return http.JsonResponse(context)







  
