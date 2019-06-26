from goods.models import SKU,GoodsCategory, SPUSpecification, SPU, SpecificationOption, SKUSpecification
from rest_framework import serializers
from django.db import transaction

#1-1,商品sku的规格信息，序列化器
class SKUSpecificationSerializer(serializers.Serializer):
    spec_id=serializers.IntegerField()
    option_id=serializers.IntegerField()


#1-2,获取sku信息的序列化器
class SKUSerializer(serializers.ModelSerializer):

    #1,重写spu,spu_id
    spu=serializers.StringRelatedField(read_only=True)
    spu_id=serializers.IntegerField()
    #2,重写category,category_id
    category=serializers.StringRelatedField(read_only=True)
    category_id=serializers.IntegerField()
    #3,specs，嵌套
    specs=SKUSpecificationSerializer()

    class Meta:
        model = SPUSpecification
        fields = "__all__"
    #4,重写create方法
    @transaction.atomic
    def create(self,validated_data):
        #0,设置保存点
        sid=transaction.savepoint()
        try:
            #1,创建sku对象
            sku=SKU.objects.create(**validated_data)
            #2,创建规格对象，并联sku
            specs=self.context["request"].data["specs"]
            for spec_dict in specs:
                SKUSpecification.objects.create\
                    (sku=sku,spec_id=spec_dict["spec_id"],option_id=spec_dict["option_id"])
        except Exception:
            transaction.savepoint_rollback(sid)
            raise serializers.ValidationError("创建失败")
        else:
            #3,返回响应;提交事务
            transaction.savepoint_commit(sid)
            return sku
    #5,重写update方法
    @transaction.atomic
    def update(self, instance, validated_data):
        #1,设置保存点
        sid=transaction.savepoint()
        try:
            #2,更新sku其他数据（价格，副标题）
            SKU.objects.filter(id=instance.id).update(**validated_data)
            # sku=SKU.objects.get(id=instance.id)
            #3,创建规格对象，关联sku
            specs=self.context["request"].data["specs"]
            for spec_dict in specs:
                SKUSpecification.objects.filter(sku_id=instance.id,spec_id=
                spec_dict["spec_id"]).update(option_id=spec_dict["option_id"])
        except Exception:
            transaction.savepoint_rollback(sid)
            raise serializers.ValidationError("更新失败")
        else:
            #4提交事务并返回
            transaction.savepoint_commit(sid)
            return SKU.objects.get(id=instance.id)



#2,获取sku三级分类，序列化器
class SKUCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields=("id","name")

#3,获取spu信息，序列化器
class GoodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model=SPU
        fields=("id","name")

#4.1获取spu规格信息
class SpecificationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpecificationOption
        fields=("id","value")

#4获取spu规格信息
class SPUSpecsSerializer(serializers.ModelSerializer):
    #spu,spu_id
    spu=serializers.StringRelatedField(read_only=True)
    spu_id=serializers.IntegerField()
    # options选项
    options=SpecificationOptionSerializer(read_only=True,many=True)
    class Meta:
        model=SPUSpecification
        exclude=("create_time","update_time") #排除字段

        



