#!/usr/bin/env python
#coding:utf-8
import urllib
import urllib2
import cookielib

class ZabbixGraph(object):
    def __init__(self, name, passwd, url="http://172.28.17.67/index.php"):
        self.url = url
        self.name = name
        self.passwd = passwd
        # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        # 定义登录所需要用的信息，如用户名、密码等，使用urllib进行编码
        login_data = urllib.urlencode({
                "name":self.name,
                "password":self.passwd,
                "autologin":1,
                "enter":"Sign in"
        })
        req = urllib2.Request(url, login_data)
        try:
            opener.open(req, timeout=10)
            self.opener = opener
        except urllib2.HTTPError,e:
            print e

    def getGraph(self,url, values, image_dir="../static/image/monitor"):
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        urlOpener = self.opener.open(request)
        image = urlOpener.read()
        image_name = "%s/%s_%s.jpg" %(image_dir, values["graphid"],values["stime"])
        f = open(image_name,"wb")
        f.write(image)

if __name__ == '__main__':
    graph = ZabbixGraph("Admin","zabbix")
    url = "http://172.28.17.67/chart2.php"
    values = {'width': 800, 'height': 200, 'graphid': '570', 'stime': '20170323153609', 'period': 3600}
    graph.getGraph(url,values)