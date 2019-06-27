from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import sku_image_serializers
from goods.models import SKUImage, SKU
from django.conf import settings
from meiduo_mall.utils.fdfs.MyFileStorage import Storage
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
    #2,重写create，上传图片
    def create(self, request, *args, **kwargs):
        #1,获取图片，sku_id参数
        sku_id=request.data.get("sku")
        image=request.data.get("image")
        #2,获取序列化器校验数据,校验
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #3,入库，上传图片
        image_url=Storage().save(None,image)
        if not image_url :
            return Response({"errmsg":"上传失败"},status=400)

        #3.4 入库
        SKUImage.objects.create(sku_id=sku_id,image=image_url)

        #4,返回响应
        return Response(status=201)



