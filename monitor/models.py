#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ZabbixMonitor(models.Model):
    name = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=20)
    ping = models.IntegerField(null=True)
    diskc = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    diskd = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.name.decode('utf-8')


class HostGroups(models.Model):
    name = models.CharField(max_length=32, verbose_name=u"主机组名")
    flags = models.IntegerField(verbose_name=u"标记")
    groupid = models.IntegerField(verbose_name=u"主机组id")

    def __str__(self):
        return self.name.encode("utf-8")

    class Meta:
        verbose_name = u"主机组"
        verbose_name_plural = u"主机组"

class Templates(models.Model):
    name = models.CharField(max_length=32, verbose_name=u"模板名")
    flags = models.IntegerField(verbose_name=u"标记")
    templateid = models.IntegerField(verbose_name="模板id")

    def __str__(self):
        return self.name.encode("utf-8")

    class Meta:
        verbose_name = u"模板"
        verbose_name_plural = u"模板"

class Host(models.Model):
    hostname = models.CharField(max_length=32, verbose_name=u"主机名称")
    ip = models.CharField(max_length=32, verbose_name=u"ip地址")
    hostid = models.IntegerField(verbose_name="主机id")
    hostgroup_id = models.ForeignKey(HostGroups, verbose_name=u"主机组id")
    template_id = models.ForeignKey(Templates, blank=True, null=True, verbose_name=u"模板id")
    available = models.IntegerField(default=0, verbose_name=u"是否可用")    # 1代表可用  0 代表不可用

class Ping(models.Model):
    host = models.ForeignKey("Host")
    ping = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)

class CpuJumps(models.Model):
    host = models.ForeignKey(Host, verbose_name=u"监控主机")
    context_switchs_per_second = models.IntegerField(verbose_name=u"每秒上下文切换次数")
    interrupts_per_second = models.IntegerField(verbose_name=u"每秒中断次数")
    date = models.DateTimeField(auto_now_add=True)

class CpuUtilization(models.Model):
    host = models.ForeignKey("Host")
    cpu_idle_time = models.CharField(max_length=16, verbose_name=u"CPU空闲百分比")
    cpu_user_time = models.CharField(max_length=16, verbose_name=u"CPU用户百分比")
    cpu_system_time =models.CharField(max_length=16, verbose_name=u"CPU系统百分比")
    cpu_iowait_time = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now_add=True)

class DiskUsage(models.Model):
    host = models.ForeignKey("Host")
    total_disk_space = models.CharField(max_length=16, verbose_name=u"磁盘总空间大小")
    free_disk_space = models.CharField(max_length=16, verbose_name=u"磁盘剩余空间大小")
    date = models.DateTimeField(auto_now=True)

class MemoryUsage(models.Model):
    host = models.ForeignKey("Host")
    total = models.CharField(max_length=16, verbose_name=u"总内存")
    free = models.CharField(max_length=16, verbose_name=u"空闲内存")
    available_memory = models.CharField(max_length=16, verbose_name=u"可用内存")
    percent = models.CharField(max_length=16, verbose_name=u"内存使用")
    date = models.DateTimeField(auto_now_add=True)
