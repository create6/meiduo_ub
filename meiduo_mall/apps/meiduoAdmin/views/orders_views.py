from rest_framework.decorators import action
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.response import Response

from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import orders_serializers
from orders.models import OrderInfo
from rest_framework.viewsets import ReadOnlyModelViewSet

'''
#1,获取全部订单信息
class OrdersView(ListAPIView):
    pagination_class = MyPageNumberPagination
    serializer_class = orders_serializers.OrdersSerializer
    # queryset = OrderInfo.objects.all()
    def get_queryset(self):
        #1,获取过滤关键字
        keyword=self.request.query_params.get("keyword")
        #2,判断有关键字
        if keyword :
            return OrderInfo.objects.filter(order_id__contains=keyword)
        else:
            return OrderInfo.objects.all()

#2,获取单个订单信息
class OrderView(RetrieveAPIView):
    serializer_class = orders_serializers.OrderGoodsSerializer
    queryset = OrderInfo.objects.all()
  '''


#3获取全部/单个订单信息,整合上面两个功能
class OrdersReadOnlyView(ReadOnlyModelViewSet):
    pagination_class = MyPageNumberPagination
    serializer_class = orders_serializers.OrderGoodsSerializer
    #3.1
    def get_queryset(self):
        # 1,获取过滤关键字
        keyword = self.request.query_params.get("keyword")
        # 2,判断有关键字
        if keyword:
            return OrderInfo.objects.filter(order_id__contains=keyword)
        else:
            return OrderInfo.objects.all()
    #3.2
    @action(methods=['PUT'],detail=True)#action 自动生成路由：/orders/{pk}/status/
    def status(self,request,pk):
        #1,获取参数
        status=request.data.get("status")
        order=self.get_object()
        #2,校验参数
        if not status:
            return Response(status=400)
        #3,数据入库
        order.status=status
        order.save()
        #4,返回响应
        return Response(status=200)











