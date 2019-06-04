from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.main import app

#发送邮件
@app.task(bind=True,name="sendEmail")
def sendEmail(self,verify_url,email):
    #1,发送短信
    result =-1  #与前面js文件关联，状态值
    try:
        result=send_mail(subject='美多商城邮箱激活',
                  message=verify_url,
                  from_email=settings.EMAIL_FROM,
                  recipient_list=[email])
        print('result:%s'%result)

    except Exception as e:
        result = -1
    #2 判断结果
    if result == -1:
        print("正在重新发送")
        self.retry(countdown=5,max_retries=3,exc=Exception("发送短信失败！"))
