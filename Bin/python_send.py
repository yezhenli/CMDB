#coding:utf-8
import re #正则
import os #python 对系统的模块
import sys #python 对系统的模块
import json #python 封装json字符串的模块
import socket #python 套接字模块
import psutil #python 监控模块
import time
import urllib  #python 向http服务器发起请求的模块
import urllib2 #python 向http服务器发起请求的模块
import contextlib
from subprocess import PIPE,Popen  #子进程模块

def get_local_ip():
    ip = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
    return ip

class SendData:
    def __init__(self,serverHost,serverPort=8000):
        """
        serverHost 用来传递服务器的地址
        """
        self.result = {
                "System":"Linux",
                "IP":get_local_ip()
            }#作为采集数据的总的数据容器
        self.host = serverHost
        self.port = serverPort
        self.url = "http://%s:%s/monitor/save/"%(self.host,self.port) #拼接接口地址
        print(self.url)#用于调试
        self.headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
            }#请求的头信息
    def getHostName(self):
        """
            获取主机名称的
        """
        with os.popen("hostname") as f:
             self.result["Hostname"] = f.read().strip()
    def getMac(self):
        """
            获取mac地址
            ifconfig | awk -F' ' '/ether/{print $2}'
        """
        p = Popen(["ifconfig"],shell=False,stdout=PIPE) #开启子进程执行ifconfig命令，并且不适用shell,
                                                            #讲输出从定向到管道
        stdout,stderr = p.communicate() #获取输出内容
        data = stdout.strip()  #对输出的内容进行两端去空
        mac = re.compile(r"ether\s[0-9a-fA-F\:]{17}") #形成匹配mac地址的正则
        for line in data.split("\n\n"): #对去空一行的内容进行切分
             macs = mac.findall(line) #对切分后的内容机械匹配
             if macs:
                 self.result["Mac"] = macs[0] #得到结果
    def getCpu(self):
        info = psutil.cpu_times()
        stats_info = psutil.cpu_stats()
        result = dict(
            user = round(info.user,2),      # 执行用户进程的时间百分比
            system = round(info.system,2),  # 执行内核进程和中断的时间百分比
            iowait = round(info.iowait,2),  # 由于IO等待而使CPU处于idle(空闲)状态的时间百分比
            idle = round(info.idle,2),      # CPU处于idle状态的时间百分比
            #log_count = psutil.cpu_count,  # 获取CPU的逻辑个数
            phy_count = psutil.cpu_count(logical=False),  # 获取CPU的物理个数
            context_switches = stats_info.ctx_switches,
            interrupts = stats_info.interrupts
        )
        self.result["CPU"] = result

    def getMem(self):
        meminfo = psutil.virtual_memory()
        swapinfo = psutil.swap_memory()
        result = dict(
            mem = dict(
                total = round(meminfo.total / (1024 ** 2),2),  # 内存总数
                available = round(meminfo.available / (1024 ** 2),2),  # 可用内存数
                used = round(meminfo.used / (1024 ** 2),2),     # 已使用的内存数
                percent = round(meminfo.percent,2),
                free=round(meminfo.free / (1024 ** 2), 2),  # 空闲内存数
                active=round(meminfo.active / (1024 ** 2), 2),  # 活跃内存数
                inactive=round(meminfo.inactive / (1024 ** 2), 2),  # 不活跃内存数
                buffers=round(meminfo.buffers / (1024 ** 2), 2),  # 缓冲使用数
                cached=round(meminfo.cached / (1024 ** 2), 2),  # 缓存使用数
                shared=round(meminfo.shared / (1024 ** 2), 2)  # 共享内存数
            ),
            swap = dict(
                total=round(swapinfo.total / (1024 ** 2), 2),  # 交换分区总数
                used=round(swapinfo.used / (1024 ** 2), 2),    # 已使用的交换分区数
                free=round(swapinfo.free / (1024 ** 2), 2),    # 空闲交换分区数
                percent=swapinfo.percent,
                sin=round(swapinfo.sin / (1024 ** 2), 2),     # 输入数
                sout=round(swapinfo.sout / (1024 ** 2), 2)    # 输出数
            )
        )
        self.result["Mem"] = result

    def getDisk(self):
        partinfo = psutil.disk_usage("/")  # 获取磁盘完整信息
        result = dict(
            free = round(partinfo.free / (1024 ** 2),2),
            used =  round(partinfo.used / (1024 ** 2),2),
            total = round(partinfo.total / (1024 ** 2),2),
            percent = round((float(partinfo.used) / partinfo.total)*100,2)
        )
        self.result["Disk"] = result

    def sendData(self):
        Data = urllib.urlencode(self.result)#对数据进行json封装
        req = urllib2.Request(self.url,data=Data,headers=self.headers)#携带请求头和请求数据发起请求
        red = urllib2.urlopen(req) #讲请求返回的内容以文件的形式进行保存
        return red.read() #打开请求返回内容



if __name__ == "__main__":
     host = sys.argv[1]
     port = sys.argv[2]
     while True:
         s = SendData(host,port) #给服务端发送数据，第一个参数为服务器端的的ip地址，第二个参数为django启动的端口8000
         s.getCpu()
         s.getDisk()
         #s.getHostName()
         #s.getMac()
         s.getMem()
         #s.getModel()
         # s.sendData()

         print(s.result)
         time.sleep(5)

