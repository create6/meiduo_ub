from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from users.models import User
from rest_framework.response import Response
from datetime import date,timedelta
from goods.models import GoodVisitCount
from meiduoAdmin.serializers import home_serializers



#1
class UserTotalCountView(APIView):
	def get(self,request):
		#1,获取用户总数
		count=User.objects.count()
		#2,返回响应
		return Response({"count":count})
#2
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