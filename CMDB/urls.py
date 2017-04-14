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
from django.conf.urls import url,include
from django.contrib import admin
from views import index,register,login,logout,forbidden,user_register_exist,prohibit

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^login/', login),
    url(r'^register/', register),
    url(r'^userRegisterExist/', user_register_exist),
    url(r'^logout/', logout),
    url(r'^404/(?P<error>\w+)/', forbidden),
    url(r'^401/$', prohibit),
    # 接口
    url(r'^api/', include('Api.urls', namespace='api')),
    # 用户
    url(r'^user/', include('User.urls', namespace='user')),
    # 日志
    url(r'^log/', include('Log.urls', namespace='log')),
    # 资产
    url(r'^assets/', include('assets.urls', namespace='assets')),
    # 监控
    url(r'^monitor/', include('monitor.urls', namespace='monitor')),
    # 权限
    url(r'^auth/', include('cmdb_auth.urls', namespace='auth')),
    # 运维管理
    url(r'^salt/', include('salt.urls', namespace='salt')),
]
