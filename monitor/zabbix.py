#!/usr/bin/env python
#coding:utf-8
from Api import zabbix_graph_api,zabbix_api
from CMDB.settings import ZABBIX_URL

"""
class Zabbix_Action(object):
    def __init__(self):
        self.url = ZABBIX_URL
        self.zabbix = zabbix_api.Zabbix_API(self.url)

    def hostgroup_sql(self):
        '''通过zabbix api获取主机组并写入数据库'''
        hostgroup_list = self.zabbix.hostgroup_get()
        for h in hostgroup_list:
            hostgroup = HostGroups()
            hostgroup.name = hostgroup["name"]
            hostgroup.flags = hostgroup["flags"]
            hostgroup.groupid = hostgroup["groupid"]
            hostgroup.save()
        return "Success"
"""




