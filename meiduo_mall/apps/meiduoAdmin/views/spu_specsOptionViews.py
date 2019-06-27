from rest_framework.viewsets import ModelViewSet
from meiduoAdmin.my_paginate import MyPageNumberPagination
from goods.models import SpecificationOption,SPUSpecification
from meiduoAdmin.serializers import spu_specs_options_serializers
from rest_framework.generics import ListAPIView

#1,规格选项
class SpuSpecOptionView(ModelViewSet):

    pagination_class = MyPageNumberPagination
    serializer_class = spu_specs_options_serializers.SpuSpecsOptionsSerializer
    queryset = SpecificationOption.objects.all()


#2,获取spu的规格信息
class SpuSpecsView(ListAPIView):
    serializer_class =spu_specs_options_serializers.SpuSpecSerializer
    # queryset = SPUSpecification

    def get_queryset(self):
        queryset=SPUSpecification.objects.all()
        for spu_spec in queryset:
            spu_spec.name = "%s-%s"%(spu_spec.spu.name,spu_spec.name)
        return queryset


