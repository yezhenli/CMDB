#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=32,verbose_name="用户名")

    password = models.CharField(max_length=32,verbose_name="密码")

    email = models.EmailField(verbose_name="邮箱")

    phone = models.CharField(max_length=28,verbose_name="手机号",blank=True,null=True)

    photo = models.ImageField(upload_to="image/userPhoto",verbose_name="头像",blank=True,null=True)

    is_lock = models.CharField(max_length=4, verbose_name="用户锁定状态")  #锁定 Y  未锁定 N

    join_date = models.DateTimeField(blank=True,null=True, verbose_name="用户注册日期")

    last_login = models.DateTimeField(blank=True,null=True, verbose_name="上次登录日期")

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")    #删除 Y  未删除 N


    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"

    def __str__(self):
        return self.username

"""
class Group(models.Model):

    name = models.CharField(max_length=32,verbose_name="组名")

    comment = models.CharField(max_length=64, verbose_name="组信息", blank=True, null=True)

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")

    class Meta:
        verbose_name = u'组信息'
        verbose_name_plural = u"组信息"

    def __str__(self):
        return self.name

class Permission(models.Model):

    name = models.CharField(max_length=32,verbose_name="权限名称")

    name_cn = models.CharField(max_length=32, verbose_name="权限中文名称")

    url = models.CharField(max_length=32, verbose_name="权限url路径")

    comment = models.CharField(max_length=128, verbose_name="权限说明", blank=True, null=True)

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")

    class Meta:
        verbose_name = u'权限信息'
        verbose_name_plural = u"权限信息"

    def __str__(self):
        return '%s(%s)' %(self.name, self.name_cn)

class UserGroup(models.Model):

    user_id = models.IntegerField(verbose_name="用户id")

    group_id = models.IntegerField(verbose_name="组id")

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")

class UserPermission(models.Model):

    user_id = models.IntegerField(verbose_name="用户id")

    permission_id = models.IntegerField(verbose_name="权限id")

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")

class GroupPermission(models.Model):

    group_id = models.IntegerField(verbose_name="组id")

    permission_id = models.IntegerField(verbose_name="权限id")

    delete_flag = models.CharField(max_length=4, verbose_name="删除标志")
"""