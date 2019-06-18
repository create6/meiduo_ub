import json
import random
import re
from django import http
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU
from .models import User, Address
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView
#类视图,注册
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self, request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # password2 = request.POST.get('password2')
        # mobile = request.POST.get('mobile')
        # allow = request.POST.get('allow')
        #1.获取参数
        user_name = request.POST.get("user_name")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        phone = request.POST.get("phone")
        msg_code = request.POST.get("msg_code")
        allow = request.POST.get("allow")

        # 2.校验参数
        # 2-1判断参数是否齐全
        if not all([user_name, pwd, cpwd, phone,msg_code,allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 2-2判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', user_name):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 2-3判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 2-4判断两次密码是否一致
        if pwd != cpwd:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 2-5判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        #2-6判断短信验证码正确性
        redis_conn= get_redis_connection("code")
        # 对应verifications/views.py中 已经存入redis
        redis_sms_code = redis_conn.get("sms_code_%s"%phone)
        #判断是否过期
        if not redis_sms_code :
            return http.HttpResponseForbidden("验证码已过期")
        #判断验证码是否相同
        if msg_code != redis_sms_code.decode():

            # return http.HttpResponseForbidden("短信验证错误"),  前后端均使用ajax提交与返回，界面会友好一些
            return redirect("/register")

        # 2-7判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 3创建对象，保存数据至数据库
        User.objects.create_user(username=user_name, password=pwd, mobile=phone)
        #异常处理
        # try:
        #
        #     User.objects.create_user(username=user_name, password=pwd, mobile=phone)
        # except DatabaseError:
        #     return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # # 响应注册结果
        # return http.HttpResponse('注册成功，重定向到首页')

        #4,返回响应
        response = redirect("/")
        return response

# chachong检查用户名是否重复
class CheckUsernameView(View):
    def get(self,request,username):
        #1,根据用户名,查询用户数量
        # print(username)
        count = User.objects.filter(username=username).count()
        # p1 = User.objects.filter(username='bo123')
        # print(count)
        # print(p1)
        #2,返回响应
        data = {
            "count":count
        }
        return http.JsonResponse(data)
#check mobile
class CheckMobileView(View):
    def get(self,request,mobile):
        #1,根据手机号,查询用户数量
        count = User.objects.filter(mobile=mobile).count()

        #2,返回响应
        data = {
            "count":count
        }
        return http.JsonResponse(data)

#登录,此处post方法中可以加入合并购物车功能
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        #1 获取参数
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        #记住密码单选项
        remembered = request.POST.get("remembered")

        # 2.校验参数
        # 2-1判断参数是否齐全
        if not all([username, pwd]):
            return http.HttpResponseForbidden('请填齐资料')

        #用户名及密码格式校验
            # 2,2 用户名格式校验
        #若涉及用手机号（多账号）时会～～～
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden("用户名格式有误")

            # 2,3 密码格式校验
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden("密码格式有误")
        # # 判断是否是会员
        # count = User.objects.filter(username=username).count()
        # if count ==0:
        #     return http.HttpResponseForbidden('请输入正确的用户名')
        # #判断密码是否正确
        # c_pwd = User.objects.filter(username=username).password
        # if pwd != c_pwd:
        #     return http.HttpResponseForbidden('密码错误')

        #2.4校验用户名及密码的正确性,使用django的authenticate方法
        #方法1  可以通过加入方法，实现多账号登录
        user =authenticate(request,username=username,password=pwd)

        # #方法2 用此传统方法只能使用用户名登录无法用手机登录
        # user =User.objects.get(username=username)
        # user.check_password(pwd)

        if not user:
            return http.HttpResponseForbidden("账号或者密码错误")

        #3 状态保持
        login(request,user)
        #3.1设置状态保持的时间
        if remembered =="on":
            request.session.set_expiry(3600*24*2)
        else:
            request.session.set_expiry(0)

        from carts.utils import merge_cookie_redis_cart
        #登录成功
        response = redirect("/")
        response.set_cookie("username",user.username,3600*24*2)
        #合并购物车
        response=merge_cookie_redis_cart(request,user,response)
        return response

#logout
class LogoutView(View):
    def get(self,request):
        # return render(request,'index.html')

        #清除session
        logout(request)

        response= redirect("/")
        #清除cookie
        response.delete_cookie("username")
        return response

#info,用户中心, View改成Mixin类
class UserCenter(MyLoginRequiredMiXinView):
    def get(self,request):
    #1 用is_authenticate 判断用户是否登陆
        if request.user.is_authenticated:
            #读取用户的username /mobile参数
            # username=request.get("username")
            # mobile=user.mobile      ,context={"username":username}
            #返回
            # print(request.user.username)
            # username=request.user.username
                #"email_active":request.user.email_active
            context = {"username": request.user.username,
                       "mobile": request.user.mobile,
                       "email":request.user.email,
                       "email_active":request.user.email_active
                       }
            return render(request,'user_center_info.html',context=context)
        #未登录，清除cookie
        else:
            response=redirect("/")
            response.delete_cookie('username')
            return response

#用户中心,add email and send verify mail
class SendEmail(MyLoginRequiredMiXinView):

    def put(self, request):  #参考 user_center_info.js
        # 1,获取邮箱
        dict_data = json.loads(request.body.decode())
        email = dict_data.get("email")
        # 2,校验参数
        # 2.1 为空校验
        if not email:
            return http.HttpResponseForbidden("参数不全")
        # 2.2 格式校验
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden("邮件格式有误")
        # 3,发送邮件    1362254116@qq.com
        # test send emil
        # send_mail(subject='你好',
        #           message='树林',
        #           from_email=settings.EMAIL_FROM,
        #           recipient_list=[email])

        # 3,发送邮件
        from meiduo_mall.utils.email import generate_verify_url
        from celery_tasks.email.tasks import sendEmail
        #调用加密
        verify_url = generate_verify_url(request.user)
        print(verify_url)
        # #调用celery队列发送
        sendEmail.delay(verify_url, email)  # celery发送邮件

        #普通发送
        # send_mail(subject='美多商城邮箱激活',
        #           message=verify_url,
        #           from_email=settings.EMAIL_FROM,
        #           recipient_list=[email])
        print('already send email')

        # 4,数据入库
        request.user.email = email
        request.user.save()

        # 5,返回响应
        return http.JsonResponse({"code": 0, "errmsg": "ok"})
#激活邮箱
class EmailActiveView(View):
    def get(self,request):
        #get token
        token=request.GET.get("token")
        print(token)
        #校验参数
        if not token:
            return http.HttpResponseForbidden("token丢失")
        #decode-token
        from utils.email import decode_token
        user=decode_token(token)
        print(user)
        if not user:
            return http.HttpResponseForbidden("token过期")
        #修改数据库PRIMARY
        user.email_active=True   #未被执行
        print(user.email_active)
        user.save()
        #返回响应（重定向至个人中心）
        return redirect('/info')

#查看address
class AddressView(MyLoginRequiredMiXinView):
    def get(self, request):
        # 1,获取用户所有的地址
        addresses = request.user.addresses.filter(is_deleted=False)

        # 2,数据拼接
        addresses_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email,
            }
            addresses_list.append(address_dict)

        context = {
            "addresses": addresses_list,
            "default_address_id": request.user.default_address_id
        }

        # 3,返回渲染页面
        return render(request, 'user_center_site.html', context=context)

# add new address
class NewAddressView(MyLoginRequiredMiXinView):
    def post(self, request):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        title = dict_data.get("title")
        receiver = dict_data.get("receiver")
        province_id = dict_data.get("province_id")
        city_id = dict_data.get("city_id")
        district_id = dict_data.get("district_id")
        place = dict_data.get("place")
        mobile = dict_data.get("mobile")
        tel = dict_data.get("tel")
        email = dict_data.get("email")

        # 2,校验参数,固话与email非必须
        if not all([title, receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden("参数不全")

        # 3,数据入库
        dict_data["user"] = request.user
        address = Address.objects.create(**dict_data)

        # 4,返回响应
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email,
        }
        return http.JsonResponse({"code": 0, "address": address_dict})

#set default address
class SetDefaultAddView(MyLoginRequiredMiXinView):
    #获取参数
    def put(self,request,defaultAdd):
        # 入库
        request.user.default_address_id=defaultAdd
        request.user.save()
        #响应
        return http.JsonResponse({"code": 0})

#update address   modify and delete
class UpdateADDView(MyLoginRequiredMiXinView):
    #modify
    def put(self, request, address_id):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        title = dict_data.get("title")
        receiver = dict_data.get("receiver")
        province_id = dict_data.get("province_id")
        city_id = dict_data.get("city_id")
        district_id = dict_data.get("district_id")
        place = dict_data.get("place")
        mobile = dict_data.get("mobile")
        tel = dict_data.get("tel")
        email = dict_data.get("email")

        # 2,校验参数
        if not all([title, receiver, province_id, city_id, district_id, place, mobile, tel, email]):
            return http.HttpResponseForbidden("参数不全")

        # 3,数据入库
        address = Address.objects.get(id=address_id)
        address.title = title
        address.receiver = receiver
        address.province_id = province_id
        address.city_id = city_id
        address.district_id = district_id
        address.place = place
        address.mobile = mobile
        address.tel = tel
        address.email = email
        address.save()

        # 4,返回响应
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email,
        }
        return http.JsonResponse({"code": 0, "address": address_dict})


    def delete(self, request, address_id):
        # 1,获取地址对象
        address = Address.objects.get(id=address_id)

        # 2,修改地址的is_deleted属性,入库
        address.is_deleted = True
        address.save()

        # 3,返回响应
        return http.JsonResponse({"code": 0})

#add address of title
class AddressTitleView(MyLoginRequiredMiXinView):
    def put(self,request,address_id):
        # address_id = request.address_id
        #1获取参数
        title=json.loads(request.body.decode()).get("title")
        #2为空校验
        if not title:
            return http.HttpResponseForbidden("参数不全")
        #3数据入库
        ret=Address.objects.filter(id=address_id).update(title=title)
        if ret ==0:
            return http.HttpResponseForbidden("修改失败")
        #4返回响应
        return http.JsonResponse({"code":0})

#modify password
class ModifyPassWordView(MyLoginRequiredMiXinView):
    def get(self,request):
        return render(request, 'user_center_pass.html')

    # def put(self,request):
    #
    #     pass

#BrowseHistoryView
class BrowseHistoryView(MyLoginRequiredMiXinView):
    #保存浏览记录
    def post(self,request):
        #1获取参数
        dict_data=json.loads(request.body.decode())
        sku_id=dict_data.get("sku_id")
        user=request.user

        #2校验参数
        if not sku_id:
            return http.HttpResponseForbidden("参数不全")
        try:
            sku=SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不存在")
        #3数据入库
        redis_conn=get_redis_connection("history")
        #3.1 去重
        redis_conn.lrem("history_%s"%user.id,0,sku_id)

        #3.2 存储
        redis_conn.lpush("history_%s"%user.id,sku_id)

        #3.3 截取
        redis_conn.ltrim("history_%s"%user.id,0,4)
        #4返回响应
        return http.JsonResponse({"code":0,"errmsg":"ok"})

    #获取浏览记录，user_center_info.js 中发出的请求
    #存取的数据名称要一致
    def get(self,request):
        #1,获取redis中的数据
        redis_conn=get_redis_connection("history")
        sku_ids=redis_conn.lrange("history_%s"%request.user.id,0,4)
        #2数据拼接
        sku_list=[]
        for sku_id in sku_ids:
            sku=SKU.objects.get(id=sku_id)
            sku_dict={
                "id":sku.id,
                "default_image_url":sku.default_image_url.url,
                "name":sku.name,
                "price":sku.price,
            }
            sku_list.append(sku_dict)

        #3返回
        return http.JsonResponse({"skus":sku_list})

#进入忘记密码页面
class ForgotPwdView(View):
    def get(self,request):

        return render(request,"find_password.html")

#忘记密码页面1
class ForgotPwd1View(View):
    def get(self,request,username):
        #1获取参数
        image_code = request.GET.get("text")
        image_code_id = request.GET.get("image_code_id")
        #2校验参数
        #2.1为空
        if not all([username,image_code,image_code_id]):
            return http.JsonResponse("参数不全")
        #2.2格式
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username) or re.match(r'^[1][3-9]\d{9}$', username):
            return http.JsonResponse("格式错误")
        #2.3用户名存在在判断，用户名或者手机号
        try:
            if re.match('^1[3-9]\d{9}$', username):
                # 手机号登录
                user = User.objects.get(mobile=username)
            else:
                # 用户名登录
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            #用户不存在
            return http.JsonResponse({"status":401})

        #验证图片验证码正确性
        # 2.2 校验图片验证码正确性，要取出redis中的值
        redis_conn = get_redis_connection("code")
        # redis_image_code 是二进制参数，需要转换
        redis_image_code = redis_conn.get("image_code_%s/" % image_code_id)
        # 2.3 判断是否过期
        if not redis_image_code:
            return http.JsonResponse({"status":4001})
        # 删除图片，防止重新验证
        redis_conn.delete("image_code_%s" % image_code_id)
        # 判断图片验证码正确性,两者都转化为小写进行比较,
        if image_code.lower() != redis_image_code.lower().decode():
            return http.JsonResponse({"status":4001})

        #返回及响应
        mobile=user.mobile
        return http.JsonResponse({"mobile":mobile})

#忘记密码页面2.1
class ForgotPwd2View(View):
    def get(self,request):
        #1获取参数
        mobile = request.GET.get("mobile")
        #2校验参数
        if not re.match(r'^[1][3-9]\d{9}$', mobile):
            return http.JsonResponse("phone_num error")
        redis_conn=get_redis_connection("code")
        # 判断短信是否发送频繁
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            return http.JsonResponse({
                "errmsg": "频繁发送", "code": 10
            })
        # 2.2生成6位随机数字
        sms_code = "%06d" % random.randint(0, 999999)

        # 2.3使用celery发送短信
        from celery_tasks.send_message.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, 5)
        print("sms_code=%s!!!" % sms_code)
        # 4 pipeline 通过减少客户端与Redis的通信次数来实现降低往返延时时间
        # 保存至redis中
        pipeline = redis_conn.pipeline()  # 保存
        pipeline.setex("sms_code_%s" % mobile, 300, sms_code)
        pipeline.setex("send_flag_%s" % mobile, 60, 1)
        pipeline.execute()  # 提交

        return http.JsonResponse({"sms_code":sms_code})


#忘记密码页面2.2   accounts/bo009/password/token/?sms_code=295090
class ForgotPwd22View(View):
    def get(self,request,username):
        #通过username取得user对象
        user=User.objects.get(username=username)
        mobile=user.mobile

        #1 获取参数
        #表单传参
        sms_code=request.GET.get("sms_code")
        #redis真实数据
        redis_conn=get_redis_connection("code")
        sms_code_id=redis_conn.get("sms_code_%s" % mobile)

        #判断短信验证码正确性
        if sms_code != sms_code_id.decode():
            return http.JsonResponse({"status":400})

        user_id=user.id

        return http.JsonResponse({"user_id":user_id})

#3页面3  ForgotPwd3View  POST /users/1/password/
class ForgotPwd3View(View):
    def post(self,request,user_id):
        #1获取参数
        # password = request.POST.get("password")
        # password2 = request.POST.get("password2")
        dict_data = json.loads(request.body.decode())
        password = dict_data.get("password")
        password2 = dict_data.get("password2")

        #2校验参数
        if not all([password,password2]):
            return http.JsonResponse({"status":400})

        if  password != password2:
            return http.JsonResponse({"status":404})
        #2.3用户存在性
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return http.JsonResponse({"status":401})
        #3.修改参数
        user.set_password(password)
        #保存
        user.save()

        #4返回响应
        return http.JsonResponse({"code":0})
        



