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
from cmdb_auth.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 角色列表
    url(r'cmdb/$', auth_index, name='cmdb'),
    # 角色管理
    url(r'cmdb/add', cmdb_add),
    # 权限管理
    url(r'cmdb/delete_auth', delete_auth),
    url(r'cmdb/group_auth/(?P<gid>[^/]+)/$', add_auth),
    # 成员管理
    url(r'cmdb/group_user/(?P<gid>[^/]+)/$', add_group_user),
    url(r'cmdb/group_auth_edit/(?P<gid>[^/]+)/$', edit_auth),
]
