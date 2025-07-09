
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *

app_name = 'goods'


urlpatterns = [
    re_path(r'^index$', IndexView.as_view(), name='index'), #首页
    re_path(r'^goods/(?P<goods_id>\d+)$',DetailView.as_view(),name='detail'), #详情页
    path('list/<int:type_id>/<int:page>/', ListView.as_view(), name='list'),


]
