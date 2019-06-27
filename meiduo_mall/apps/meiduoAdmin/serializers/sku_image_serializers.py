from rest_framework import serializers
from goods.models import SKUImage, SKU


#1,图片管理序列化器
class SKUImageSerializer(serializers.ModelSerializer):

    class Meta:
        model=SKUImage
        fields= "__all__"

#2,获取sku信息
class SKUSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model=SKU
        fields=("id","name")



        



