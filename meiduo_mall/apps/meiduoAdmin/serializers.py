from rest_framework import serializers
from goods.models import GoodVisitCount, GoodsCategory, SPU

#1,定义日分类访问量，
from users.models import User


class UserGoodsDaySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GoodVisitCount
        fields = ("count","category")

#2,获取用户信息，序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoodsDaySerializer
        fields=("id","username","mobile","email")


# 3,新增用户,序列化器
class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "mobile", "email", "password")

        # 1,添加额外的约束,不返回密码
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # 1,重写create方法,加密密码
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



#4-1,商品sku的规格信息，序列化器
class SKUSpecificationSerializer(serializers.Serializer):
    spec_id=serializers.IntegerField()
    option_id=serializers.IntegerField()


#4-2,获取sku信息的序列化器
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
        model = SKUSerializer
        fields = "__all__"

#5,获取sku三级分类，序列化器
class SKUCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields=("id","name")

#6,获取spu信息，序列化器
class GoodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model=SPU
        fields=("id","name")


