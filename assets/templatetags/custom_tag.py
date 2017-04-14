#coding:utf-8
__author__ = 'jieli'
import datetime
import re
from django import template
from assets.models import Cabinet,Rack
from monitor.models import *

register = template.Library()


@register.filter
def sum_size(data_set):
    total_val = sum([i.capacity if i.capacity else 0 for i in data_set])

    return total_val

@register.filter
def list_count(data_set):
    data_count = len([i.capacity if i.capacity else 0 for i in data_set])

    return data_count

@register.filter
def rack_count(data_set,cabinet_id):
    '''统计机架数量'''
    total_count = len([i if i.cabinet_id == cabinet_id else 0 for i in data_set])
    return total_count

@register.filter
def disk_usage(data_set):
    '''统计磁盘使用率'''
    if len(data_set) != 0:
        i = data_set[len(data_set)-1]
        total_disk_space = i.total_disk_space
        free_disk_space = i.free_disk_space
        diskUsage = round((float(total_disk_space)-float(free_disk_space)) / float(total_disk_space)*100,2)
    else:
        diskUsage = "unknown"
    return diskUsage

@register.filter
def mem_usage(data_set):
    if len(data_set) != 0:
        i = data_set[len(data_set)-1]
        memUsage = i.percent
    else:
        memUsage = "unknown"
    return memUsage


@register.simple_tag
def get_time_humanize_display(time_seconds):
    if time_seconds < 60:
        return '%s秒'%time_seconds
    elif time_seconds < 60*60:
        return '%s分' % (time_seconds/60)

    elif time_seconds < 60 * 60 * 24:
        return '%s小时' % (time_seconds /60/60)

@register.filter
def ping(data_set):
    ping_val = sum([i.ping if i.ping else 0 for i in data_set])
    return ping_val

