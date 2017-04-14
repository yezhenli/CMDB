#!/usr/bin/env python
# -*- coding:utf-8 -*-

from CMDB.settings import SHELLINABOX
import paramiko
import sys


class Myclient(object):
    def __init__(self,username, passwd, port=22):
        self.username = username
        self.passwd = passwd
        self.port = port
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=SHELLINABOX['host'],
            username=self.username,
            password=self.passwd,
            port=self.port
        )

    def login(self,hostname,username,password):
        command = "ssh %s@%s\n" %(username,hostname)
        channel = self.ssh.invoke_shell()
        channel.settimeout(2)
        channel.send(command)

        while True:
            try:
                recv_data = channel.recv(9999)
                if recv_data:
                    print_data = recv_data.splitlines()[:-1]
                    if isinstance(print_data,str):
                        print print_data
                    elif isinstance(print_data,list):
                        print "\n".join(print_data)
                    else:
                        continue
                else:
                    continue
            except Exception as e:
                control = raw_input(recv_data.splitlines()[-1])
                if control == "break":
                    channel.close()
                    self.ssh.close()
                    sys.exit()
                else:
                    channel.send(control+"\n")

if __name__ == '__main__':
    m = Myclient("root","123456")
    m.login("192.168.1.68","root","123456")