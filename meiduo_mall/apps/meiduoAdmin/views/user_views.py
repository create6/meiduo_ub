
from rest_framework.generics import ListAPIView, CreateAPIView
from meiduoAdmin.my_paginate import MyPageNumberPagination
from meiduoAdmin.serializers import user_serializers


#7用户查询获取，,CreateAPIView --增加用户类视图
from users.models import User


class UserView(ListAPIView,CreateAPIView):
	# serializer_class = UserSerializer
	# queryset = User.objects.all()
	pagination_class =  MyPageNumberPagination

	# 1,重写获取序列化器的方法
	def get_serializer_class(self):
		if self.request.method == "GET":
			return user_serializers.UserSerializer
		else:
			return user_serializers.UserAddSerializer

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