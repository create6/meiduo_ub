from rest_framework.viewsets import ModelViewSet
from meiduoAdmin.my_paginate import MyPageNumberPagination
from goods.models import SPUSpecification
from meiduoAdmin.serializers import spu_specs_serializers



#1,商品规格的操作(增删改查，全功能)
class SpuSpecView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    serializer_class = spu_specs_serializers.SpuSpecSerializer
    queryset = SPUSpecification.objects.all()




