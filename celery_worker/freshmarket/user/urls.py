
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


app_name = 'user'  #反向解析，会用到  reverse('user:login') 中的 user，后面的
# login 就是路由地址后面的 name 属性


urlpatterns = [
    re_path(r'^register$', RegisterView.as_view(), name='register'),  #注册页面
    re_path(r'^login$',LoginView.as_view(),name='login'),
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),  #用户激活地址

    #path('register_handle/', register_handle, name='register_handle'),








]
