from rest_framework import serializers
from goods.models import SpecificationOption,SPUSpecification

#1,规格选项
class SpuSpecsOptionsSerializer(serializers.ModelSerializer):
    #1,spec,spec_id
    spec=serializers.StringRelatedField(read_only=True)
    spec_id=serializers.IntegerField()

    class Meta:
        model=SpecificationOption
        fields="__all__"


#2,spu规格
class SpuSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model=SPUSpecification
        fields=("id","name")