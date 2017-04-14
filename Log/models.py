#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from User.models import User
from assets.models import Server


# Create your models here.
"""
class Plan(models.Model):
    '''store all task plans'''
    name = models.CharField(max_length=64, verbose_name="Plan Name")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ScheduleLog(models.Model):
    '''Store Schedule run logs '''
    plan = models.ForeignKey("Plan")
    status_choices = ((0,'failed'),(1,'success'),(2,'error'),(3,'running'))
    status = models.SmallIntegerField(choices=status_choices)
    errors = models.TextField(blank=True,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
"""

class AuditLog(models.Model):

    user = models.ForeignKey(User)
    host = models.ForeignKey(Server)
    action_choices = (
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'exception'),
    )
    action_type = models.IntegerField(choices=action_choices,default=0)
    cmd = models.TextField(blank=True,null=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'
