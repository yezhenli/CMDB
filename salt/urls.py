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
from salt.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'command/$', command, name='command'),

    # 命令执行
    url(r'execute/(?P<server_id>[0-9]+)/$', execute, name='execute'),
    url(r'execute_fun/(?P<server_id>[0-9]+)/$', execute_fun, name='execute_fun'),

    # 客户端管理
    url(r'minions/(?P<server_id>[0-9]+)/$', minions, name='minions'),
    url(r'minions_fun/$', minions_fun, name='minions_fun'),

    # 远程文件操作
    url(r'file_remote/(?P<server_id>[0-9]+)/$', file_remote, name='file_remote'),
    url(r'file_remote_create/$', file_remote_create, name='file_remote_create'),
    url(r'file_remote_rename/$', file_remote_rename, name='file_remote_rename'),
    url(r'file_remote_write/$', file_remote_write, name='file_remote_write'),
    url(r'file_remote_delete/$', file_remote_delete, name='file_remote_delete'),

    # 执行记录
    url(r'record/$', record, name='record')
]
