from rest_framework import serializers
from orders.models import OrderInfo, OrderGoods


#1,获取订单序列化器
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderInfo
        fields="__all__"


#2.1,获取单个订单序列化器
class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        moedel=OrderGoods
        fields="__all__"
#2.2
class OrderSerializer(serializers.ModelSerializer):
    skus=OrderGoodsSerializer(read_only=True,many=True)
    class Meta:
        model=OrderInfo
        fields="__all__"