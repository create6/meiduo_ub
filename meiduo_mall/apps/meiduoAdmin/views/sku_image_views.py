from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import sku_image_serializers
from goods.models import SKUImage, SKU


#1,获取图片数据
class SkuImagesView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    serializer_class = sku_image_serializers.SKUImageSerializer
    queryset = SKUImage

    #1,获取所有的sku信息：
    def sku_simple(self,request):
        #1,查询所有的sku数据
        queryset=SKU.objects.all()
        #2,获取序列化器
        serializer=sku_image_serializers.SKUSimpleSerializer(instance=queryset,many=True)

        #3,返回响应
        return Response(serializer.data)