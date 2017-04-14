#/usr/bin/env python
#coding:utf-8
from CMDB.settings import ZABBIX
import json
import urllib
import urllib2

class Zabbix_API(object):

    def __init__(self, url):
        self.url = url
        self.head = {"Content-Type":"application/json"}
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.7 Safari/537.36"
            }
        self.token = self.zabbix_auth(ZABBIX["user"], ZABBIX["pass"])

    def zabbix_url_request(self, data):
        '''THe method of zabbix url request'''
        jsonData = json.dumps(data)
        req = urllib2.Request(self.url, data=jsonData, headers=self.header)
        # 添加head
        for key in self.head.keys():
            req.add_header(key,self.head[key])
        try:
            ope = urllib2.urlopen(req)
        except Exception as e:
            print e
            return False
        else:
            return json.loads(ope.read())

    def zabbix_auth(self, zabbix_user, zabbix_pass):
        '''authentication and return token'''
        data = {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": zabbix_user,
                        "password": zabbix_pass
                    },
                    "id": 0
                }
        response = self.zabbix_url_request(data)
        # 如果返回数据中有result字段，则返回result数据，也即token
        if 'result' in response:
            return response["result"]
        else:
            print response['error']['data']
            return False

    def hostgroup_get(self):
        '''get hostgroup'''
        data = {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend"
                },
                "auth": self.token,
                "id": 1
                }
        # 获取所有的主机组信息
        response = self.zabbix_url_request(data)
        hostgroup_list = []
        # 如果返回数据有result字段，则表示当前Zabbix存在主机组信息，否则返回False
        if 'result' in response.keys():
            rest = response["result"]
            # 如果result字段和长度都不为0，添加groupid信息到主机组列表中
            if rest != 0 or len(rest) !=0:
                for hostgroup in rest:
                    var = {}
                    var["groupid"] = hostgroup["groupid"]
                    var["name"] = hostgroup["name"]
                    var["flags"] = hostgroup["flags"]
                    hostgroup_list.append(var)
                return hostgroup_list
            else:
                print "Get HostGroup Error,please check !"
                return False
        else:
            return False

    def template_get(self):
        '''get template'''
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
            },
            "auth": self.token,
            "id": 1
        }
        response = self.zabbix_url_request(data)
        template_list = []
        # 如果返回数据有result字段，则表示当前Zabbix存在模板信息，否则返回False
        if "result" in response.keys():
            rest = response["result"]
            # 如果result字段和长度都不为0，添加templateid信息到模板列表中
            if rest != 0 or len(rest) != 0:
                for template in rest:
                    var = {}
                    var["templateid"] = template["templateid"]
                    var["name"] = template["name"]
                    var["flags"] = template["flags"]
                    template_list.append(var)
                return template_list
            else:
                print "Get Template  Error,please check !"
                return False
        else:
            return False

    def history_get(self):
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": "23296",
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 10
            },
            "auth": self.token,
            "id": 7
        }
        response = self.zabbix_url_request(data)
        print response

    def items_get(self):
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "itemid",
                "hostids": "10122",
                "search": {
                    "key_": "system"
                },
                "sortfield": "name"
            },
            "auth": self.token,
            "id": 1
        }
        response = self.zabbix_url_request(data)
        print response

    def get_hostids(self,groupid):
        data = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": "hostid",
                    "groupids": groupid
                },
                "auth": self.token,
                "id": 5
            }
        response = self.zabbix_url_request(data)["result"]
        hostids = []
        for i in range(len(response)):
            hostids.append(response[i]['hostid'])
        return hostids

    # 根据hostid获取host的所有数据
    def get_info(self,groupid,method,info,parm=""):
        hostinfos = []
        infos = self.get_hostids(groupid)
        # for i in infos:
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": {
                "output": "extend",
                "hostids": infos[0],
                "search": {
                    "key_": parm
                },
            },
            "auth": self.token,
            "id": 2
        }
        response = self.zabbix_url_request(data)['result']
        print response
        # hostinfos.append(response[0][info] if len(response) !=0 else hostinfos.append("0"))
        return hostinfos

def main():
    url = url = "http://172.28.17.67/api_jsonrpc.php"
    zbx = Zabbix_API(url)

    zbx.items_get()

    # 获取所有主机组信息
    # hostgroup_list = zbx.hostgroup_get()
    # names = zbx.get_info("4","host.get","name")
    # ips = zbx.get_info("4","hostinterface.get","ip")
    # cpu = zbx.get_info("2","history.get","","system.cpu.util")
    # diskc = zbx.get_info("4","item.get","lastvalue","hrStorageUsage2")
    # diskd = zbx.get_info("4","item.get","lastvalue","hrStorageUsage3")
    # for a, b, c, d, e in zip(names, ips, pings, diskc, diskd):
    #     print a, b, c, d, e

if __name__ == '__main__':
    main()










