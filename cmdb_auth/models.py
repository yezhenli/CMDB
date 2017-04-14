#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from User.models import User

# Create your models here.


class auth_group(models.Model):
    """
    权限组
    """
    group_name = models.CharField(max_length=100, verbose_name=u'角色名称', unique=True)
    group_user = models.ManyToManyField(User, blank=True, verbose_name=u'所属用户')
    enable = models.BooleanField(default=True, verbose_name=u'是否启用')
    explanation = models.TextField(verbose_name=u'角色描述')
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u"角色管理"
        verbose_name_plural = verbose_name



class user_auth_cmdb(models.Model):
    """
    cmdb权限
    所有字段全部以0，1来表示
    1表示有此权限，0表示无此权限
    所有数据全部外键关联user表，当用户删除时相应权限也随之删除
    """
    u"""
    资产管理
    """
    select_host = models.BooleanField(default=False, verbose_name=u"查看资产")
    edit_host = models.BooleanField(default=False, verbose_name=u"修改资产")
    update_host = models.BooleanField(default=False, verbose_name=u"更新资产")
    add_host = models.BooleanField(default=False, verbose_name=u"添加主机")
    bat_add_host = models.BooleanField(default=False, verbose_name=u"批量添加")
    delete_host = models.BooleanField(default=False, verbose_name=u"删除资产")
    add_line_auth = models.BooleanField(default=False, verbose_name=u"产品线管理")
    u"""
    发布权限
    """
    auth_project = models.BooleanField(default=False, verbose_name=u"自动化发布")
    auth_highstate = models.BooleanField(default=False, verbose_name=u"自动化部署")

    u"""
    用户管理
    """
    add_user = models.BooleanField(default=False, verbose_name=u'添加用户')
    edit_user = models.BooleanField(default=False, verbose_name=u'修改用户')
    edit_pass = models.BooleanField(default=False, verbose_name=u"修改密码")
    delete_user = models.BooleanField(default=False, verbose_name=u"删除用户")
    add_department = models.BooleanField(default=False, verbose_name=u"部门管理")

    u"""
    机房管理
    """

    select_idc = models.BooleanField(default=False, verbose_name=u"查看机房")
    add_idc = models.BooleanField(default=False, verbose_name=u"添加机房")
    edit_idc = models.BooleanField(default=False, verbose_name=u"修改机房")
    del_idc = models.BooleanField(default=False, verbose_name=u"删除机房")

    u"""
    系统管理
    """
    setup_system = models.BooleanField(default=False, verbose_name=u"安装系统")
    upload_system = models.BooleanField(default=False, verbose_name=u"主机上报")
    salt_keys = models.BooleanField(default=False, verbose_name=u"批量管理")

    u"""
    项目管理
    """
    project_auth = models.BooleanField(default=False, verbose_name=u"项目列表")
    add_project = models.BooleanField(default=False, verbose_name=u"添加项目")
    edit_project = models.BooleanField(default=False, verbose_name=u"修改项目")
    delete_project = models.BooleanField(default=False, verbose_name=u"删除项目")

    u"""
    日志管理
    """
    auth_log = models.BooleanField(default=False, verbose_name=u"salt执行记录")
    cmdb_log = models.BooleanField(default=False, verbose_name=u"资产操作记录")
    server_audit = models.BooleanField(default=False, verbose_name=u"服务器操作记录")


    group_name = models.ForeignKey(auth_group, verbose_name=u'所属角色', help_text=u"添加角色组权限")

    def __unicode__(self):
        return self.group_name
        # return u"权限管理"

    class Meta:
        verbose_name = u"权限管理"
        verbose_name_plural = verbose_name


