from datetime import date, timedelta
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodVisitCount, SKU, GoodsCategory, SPU
from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import UserSerializer
from . import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination

#1,获取总人数
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class UserTotalCountView(APIView):
	def get(self,request):
		#1,获取用户总数
		count=User.objects.count()
		#2,返回响应
		return Response({"count":count})

class UserDayIncrementView(APIView):
	def get(self,request):
		#1,获取今天的日期
		today=date.today()
		#2,查询用户的数量
		count=User.objects.filter(date_joined__gte=today).count()
		#3,返回响应
		return Response({"count":count})
#3,日活用户数统计
class UserDayActiveView(APIView):
	def get(self,request):
		#1,获取今天的日期
		today=date.today()
		#2,查询用户的数量
		count=User.objects.filter(last_login__gte=today).count()
		#3,返回响应
		return Response({"count":count})

#4,下单用户统计
class UserDayOrdersView(APIView):
	def get(self,request):
		#1,获取今天日期
		today=date.today()
		#2,查询用户的数量
		count=User.objects.filter(orders__create_time__gte=today).count()
		#3,返回响应
		return Response({"count":count})

#5,月新增用户
class UserMonthIncrementView(APIView):
	def get(self,request):
		#1,获取当前日期
		today=date.today()
		#2,获取29天前的日期
		old_date=today - timedelta(days=29)
		#3,遍历30天
		user_date_list=[]
		for i in range(29):
			#3.1 当前时间
			current_date=old_date+ timedelta(days=i)
			#3.2 下一天
			next_date=old_date +timedelta(i+1)
			#3.3 获取每天的新增人数
			count=User.objects.filter(date_joined__gte=current_date,date_joined_lt=next_date).count()
			user_date_list.append({"count":count,"date":current_date})
			#4,返回响应
			return Response(user_date_list)

#6,日分类商品访问量
class UserGoodsDayView(GenericAPIView):
	serializer_class = serializers.UserGoodsDaySerializer
	def get_querset(self,request):
		#1,获取当天日期
		today=date.today()
		#2,返回分类访问数量
		return GoodVisitCount.objects.filter()

	def get(self,request):
		#1,查询分类访问数量
		good_visits = self.get_queryset()
		#2,获取序列化器
		serializer =self.get_serializer(instance=good_visits,many=True)
		#3,返回响应
		return Response(serializer.data)

#7用户查询获取，,CreateAPIView --增加用户类视图
class UserView(ListAPIView,CreateAPIView):
	# serializer_class = UserSerializer
	# queryset = User.objects.all()
	pagination_class =  MyPageNumberPagination

	# 1,重写获取序列化器的方法
	def get_serializer_class(self):
		if self.request.method == "GET":
			return serializers.UserSerializer
		else:
			return serializers.UserAddSerializer

	#过滤
	# queryset = User.objects.all()
	def get_queryset(self):
		# 1,获取过滤的关键字
		keyword = self.request.query_params.get("keyword")

		# 2,判断是否过滤了
		if keyword:
			return User.objects.filter(username__contains=keyword)
		else:
			return User.objects.all()
	# 添加用户 CreateAPIView --增加用户类视图
	# def post(self,request):
	# #1,获取数据
	# dict_data = request.data
	#
	# #2,获取序列化器,校验,入库
	# serializer = self.get_serializer(data=dict_data)
	# serializer.is_valid(raise_exception=True)
	# serializer.save()
	#
	# #3,返回响应
	# return Response(serializer.data,status=201)

	# 使用mixin
	# return self.create(request)

#8,获取商品sku信息
class SKUView(ModelViewSet):
	pagination_class = MyPageNumberPagination
	serializer_class = serializers.SKUSerializer
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

#9,获取商品sku分类（三级分类）
class SKUCategoryView(ListAPIView):
	serializer_class = serializers.SKUCategorySerializer
	queryset = GoodsCategory.objects.filter(subs=None)


#10,商品spu信息,列表信息
class GoodSimpleView(ListAPIView):
	serializer_class= serializers.GoodSimpleSerializer
	queryset = SPU.objects.all()




