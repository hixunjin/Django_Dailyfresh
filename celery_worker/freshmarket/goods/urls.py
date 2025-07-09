
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *

app_name = 'goods'


urlpatterns = [
    re_path(r'^index$', index, name='index')
]
