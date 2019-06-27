from rest_framework import serializers
from goods.models import SPUSpecification


#1,操作spu,序列化器
class SpuSpecSerializer(serializers.ModelSerializer):
    # 1,spu,spu_id(外键)
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    class Meta:
        model=SPUSpecification
        fields='__all__'







