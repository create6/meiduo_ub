#合并购物车功能,users/views.py--->login
'''
request:为了获取cookie数据
user：为了获取redis数据
response：为了清空cookie数据
'''
import pickle
import base64
from django_redis import get_redis_connection

def merge_cookie_redis_cart(request, user, response):
    #1获取cookie数据
    cookie_cart=request.COOKIES.get("cart")
    #2判断cookie是否存在，如有则转换
    if not cookie_cart:
        return response
    cookie_dict={}
    if cookie_cart:
        #str 转 dict
        cookie_dict=pickle.loads(base64.b64decode(cookie_cart.encode()))

    #3合并数据
    redis_conn=get_redis_connection("cart")
    #在cookie字典中遍历
    for sku_id,count_selected in cookie_dict.items():
        #设置redis数据
        redis_conn.hset("cart_%s"%user.id,sku_id,count_selected["count"])
        #
        if count_selected["selected"]:
            redis_conn.sadd("cart_selected_%s"%user.id,sku_id)
        else:
            redis_conn.srem("cart_selected_%s"%user.id,sku_id)

    #4清除cookie返回响应
    response.delete_cookie("cart")
    return response