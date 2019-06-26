from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduoAdmin.my_paginate import MyPageNumberPagination
from goods.models import SPU, Brand, GoodsCategory
from meiduoAdmin.serializers import spu_serializers
from django.conf import settings

class SPUView(ModelViewSet):
    #1-1,分页
    pagination_class = MyPageNumberPagination
    #1-2,序列化器
    serializer_class = spu_serializers.SPUSerializer
    #1-3,数据集(数据)
    queryset = SPU.objects.all()


    #2,获取品牌数据
    def brand(self,request):
        #1,查询所有品牌
        brands=Brand.objects.all()
        #2,获取序列化器
        serializer=spu_serializers.BrandSerializer(instance=brands,many=True)
        #3,返回响应
        return Response(serializer.data)

    #3,一级分类
    def category(self,request):
        #1,查询一级分类
        categories1=GoodsCategory.objects.filter(parent=None)
        #2,获取序列化器
        serializer=spu_serializers.CategorySerializer(instance=categories1,many=True)
        #3,返回响应
        return Response(serializer.data)
    #4,二三级分类
    def category_sub(self,request,pk):
        #1,获取二三级分类
        categories=GoodsCategory.objects.filter(parent_id=pk)#parent__id
        #2,获取序列化器
        serializer=spu_serializers.CategorySerializer(instance=categories,many=True)
        #3,返回响应
        # return Response(serializer.data)#改前端的情况下：(改前端this['category'+num + '_list']=dat.data.subs--->dat.data)
        return Response({"subs":"serializer.data"})

    #5,上传图片
    def upload_image(self,request):
        #1,获取参数
        image=request.FILES.get("image")
        #2,校验参数（省略）
        #3,上传图片,判断是否上传成功,断点调试，看request传递的参数/字段
        client=Fdfs_client(settings.FDFS_CONFIG)
        # result=client.upload_by_filename()
        result=client.upload_by_buffer(image.read())
        if result["Status"] != "Upload successed.":
            return Response({"errmsg":"上传失败"},status=400)
        image_url=result["Remote file_id"]  #拼接路径
        #4,返回响应
        return Response({"img_url":settings.BASE_URL + image_url})












