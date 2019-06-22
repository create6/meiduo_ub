#!/bin/bash

git add .
git commit -m 'udpate'
git push

echo 'push success!'

#bash 向python向传参
~/Desktop/myshell/source/sendEmail_1.py success push by $(pwd)





#/usr/bin/env python pushby$(pwd) <<-EOF
#import sys
#import smtplib
#from email.mime.text import MIMEText
#
#
#
#username_recv = '1362254116@qq.com'#收件人，多个收件人用逗号隔开
#content_send= sys.argv[1:]
#print('发送内容：%s'%content_send)


# mailserver = "smtp.126.com"  #邮箱服务器地址
# username_send = 'create6@126.com'  #邮箱用户名
# password = 'bolsu3306'   #邮箱密码：需要使用授权码
# #mail = MIMEText('hello python and shell')   #内容
# mail = MIMEText(content_send)   #内容
# mail['Subject'] = 'lsu_IT'
# mail['From'] = username_send  #发件人
# mail['To'] = username_recv  #收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
# smtp = smtplib.SMTP(mailserver,port=25) # 连接邮箱服务器，smtp的端口号是25
# # smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
# smtp.login(username_send,password)  #登录邮箱
# smtp.sendmail(username_send,username_recv,mail.as_string())# 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
# smtp.quit() # 发送完毕后退出smtp
# print ('success')


#EOF

