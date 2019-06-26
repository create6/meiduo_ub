from rest_framework import serializers
from goods.models import GoodVisitCount




#1,定义日分类访问量，
class UserGoodsDaySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GoodVisitCount
        fields = ("count","category")