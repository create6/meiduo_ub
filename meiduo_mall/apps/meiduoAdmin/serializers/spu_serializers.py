from rest_framework import serializers
from goods.models import SPU, Brand, GoodsCategory


#1,操作spu,序列化器
class SPUSerializer(serializers.ModelSerializer):
    #1,设置brand,brand_id,新增字段
    brand=serializers.StringRelatedField(read_only=True)
    brand_id=serializers.IntegerField()
    #2,设置category_id
    category1_id=serializers.IntegerField()
    category2_id=serializers.IntegerField()
    category3_id=serializers.IntegerField()
    class Meta:
        #3,参考模型
        model=SPU
        #4,全部字段
        # fields="__all__"
        #4,排除字段
        exclude=("create_time","update_time","category1","category2","category2")

#2,获取品牌序列化器
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields=("id","name")

#3,获取分类
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields=("id","name")









