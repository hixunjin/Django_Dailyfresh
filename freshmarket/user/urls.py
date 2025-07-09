from django.contrib import admin
from django.urls import path,include,re_path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'user'  #反向解析，会用到  reverse('user:login') 中的 user，后面的
# login 就是路由地址后面的 name 属性


urlpatterns = [
    re_path(r'^register$', RegisterView.as_view(), name='register'),  #注册页面
    re_path(r'^login$',LoginView.as_view(),name='login'),
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),  #用户激活地址

    #path('register_handle/', register_handle, name='register_handle'),

    #用户个人信息---用户订单信息---用户地址信息
    #re_path(r'^$',login_required(UserInfoView.as_view()),name='user'),
    #re_path(r'^order$',login_required(UserOrderView.as_view()),name='order'),
    #re_path(r'address$',login_required(UserAddressView.as_view()),name='address')

    ##用户个人信息---用户订单信息---用户地址信息（已经继承了 LoginRequiredMixin类）
    re_path(r'^$',UserInfoView.as_view(),name='user'),
    re_path(r'^order$',login_required(UserOrderView.as_view()),name='order'),
    re_path(r'address$',UserAddressView.as_view(),name='address'),

    #退出登录
    re_path(r'^logout$',LoginView.as_view(),name='logout'),
    re_path(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),








]
