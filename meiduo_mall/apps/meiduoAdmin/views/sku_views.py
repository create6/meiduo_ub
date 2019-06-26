from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from goods.models import SKU, GoodsCategory, SPU,SKU,SPUSpecification
from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import sku_serializers

#1,获取商品sku信息
class SKUView(ModelViewSet):
	pagination_class = MyPageNumberPagination
	serializer_class = sku_serializers.SKUSerializer
	queryset = SKU.objects.all()

	#1,重写数据源方法，过滤数据
	def get_queryset(self):
		#1,获取过滤关键字
		keyword=self.request.query_params.get("keyword")
		#2,判断是否有关键字
		if keyword:
			return SKU.objects.filter(name__contains=keyword)
		else:
			return SKU.objects.all()

#2,获取商品sku分类（三级分类）
class SKUCategoryView(ListAPIView):
	serializer_class = sku_serializers.SKUCategorySerializer
	queryset = GoodsCategory.objects.filter(subs=None)


#3,商品spu信息,列表信息
class GoodSimpleView(ListAPIView):
	serializer_class= sku_serializers.GoodSimpleSerializer
	queryset = SPU.objects.all()


#4,商品spu规格信息
class SPUSpecsView(ListAPIView):
	serializer_class=sku_serializers.SPUSpecsSerializer
	# queryset=SPUSpecification.objects.all()
	def get_queryset(self):
		#1,获取pk值
		pk=self.kwargs.get("pk")
		#2,查询商品spu规格对象
		return SPUSpecification.objects.filter(spu_id=pk)







