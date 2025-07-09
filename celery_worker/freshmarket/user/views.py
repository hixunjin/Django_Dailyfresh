import re
from email.utils import formataddr

from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.core.mail import send_mail

from celery_tasks.tasks import send_register_active_email
#显示注册页面

class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        """接收表单数据"""
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')  # 如果被选中，获取的值是 on
        confirm_password = request.POST.get('cpwd')  # 确认密码

        """数据校验"""
        if not all([username, password, email, allow]):
            return render(request, 'register.html', {"errmsg": "数据不完整"})  # 数据不完整

        """邮箱校验"""
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {"errmsg": "邮箱格式不正确！"})

        """是否勾选协议"""
        if allow != "on":
            return render(request, 'register.html', {"errmsg": "请勾选协议"})

        """校验用户名是否重复"""

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在，可用
            user = None

        if user:
            # 用户名存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 检查密码是否一致
        if password != confirm_password:
            return render(request, 'register.html', {'errmsg': '两次输入的密码不一致'})

        """全部通过，校验数据"""
        user = User.objects.create_user(username, email, password)

        #设置默认为未激活状态
        user.is_active = 0
        user.save()

        #激活链接设置
        # 发送激活邮件，包含激活连接： http：//127.0.0.1：8000/user/active/用户id
        # 激活连接中需要包含用户的身份信息，并且要把身份信息进行加密处理

        serializer = Serializer(settings.SECRET_KEY,3600)  #设置加密对象，有效时间为 1h
        info = {'confirm':user.id}
        token = serializer.dumps(info)  #对id值进行加密
        token = token.decode('utf8')

        #发送邮件，现在切换成异步处理任务，在 Celery 文件中编写好后，直接调用传参即可
        send_register_active_email.delay(email,username,token)  #需要三个参数




        # 返回到首页
        return redirect(reverse('goods:index'))


#在完成激活功能之前，我们应该把用户设置为未激活状态
#先修改下代码



#激活视图类
class ActiveView(View):
    def get(self,request,token):
        """进行解密，获取要激活的用户信息"""
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)  #解密
            user_id = info['confirm']  #获取id

            #查询处指定用户，并设置 is_active 的值为1，完成激活
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            #返回到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse("激活链接已经失效！")






#返回登录界面

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')





















