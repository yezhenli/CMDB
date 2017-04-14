#coding:utf-8
"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'server/', server_list, name='server'),
    # 资产列表
    url(r'asset_list/$', asset_list, {'page': "1"}, name='asset_list'),
    url(r'asset_list/(?P<page>\d+)', asset_list, name='asset_list'),
    url(r'type_change/', type_change, name='type_change'),
    # 资产详细信息
    url(r'asset_content/(?P<ids>\d+)', content, name='asset_content'),
    # 资产添加
    url(r'asset_add/', asset_add, name='asset_add'),
    # 机房
    url(r'idc_add/', idc_add, name='idc_add'),
    url(r'idc/$', idc, name='idc'),
    url(r'idc/(?P<idc_id>\d+)/change', idc_change, name='idc'),
    # 机柜
    url(r'cabinet/$', cabinet, name='cabinet'),
    url(r'cabinet_add/', cabinet_add, name='cabinet_add'),
    url(r'cabinet/change/', cabinet_change,),
    # 机架
    url(r'rack/', rack, name='rack'),
    url(r'rack_add/', rack_add, name='rack_add'),
]
