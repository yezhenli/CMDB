#!/usr/bin/env python
#coding:utf-8
import urllib2
import urllib
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context
#Python 2.7.9 之后版本引入了一个新特性
#当你urllib.urlopen一个 https 的时候会验证一次 SSL 证书
#当目标使用的是自签名的证书时就会爆出一个
#urllib.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)> 的错误消息

class SaltApi(object):
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')  #移除URL末尾的/
        self.__username = username
        self.__password = password
        self.__token_id = self.saltLogin()

    # 登陆获取token
    def saltLogin(self):
        params = {'eauth':'pam','username':self.__username,'password':self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content["return"][0]["token"]
            return token
        except KeyError:
            raise KeyError

    # 推送请求
    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token':self.__token_id}
        if obj:
            data,number = re.subn('arg\d*', 'arg', obj)  #将arg1 arg2这些关键字都替换成arg，number为替换次数
        else:
            data = None
        req = urllib2.Request(url, data, headers)        # obj为传入data参数字典，data为None 则方法为get，有date为post方法
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    # 执行命令
    def saltCmd(self, tgt, fun, client='local_async', expr_form='glob', arg=None, **kwargs):
        '''
        :param tgt: 目标主机对象
        :param fun: 调用的函数
        :param client:
        :param expr_form: 主机对象类型
        :param arg: 参数
        :param kwargs:
        :return:
        '''
        params = {'client':client,'fun':fun,'tgt':tgt,'expr_form':expr_form}
        if arg:
            a = arg.split(',')   # 参数按逗号分隔
            for i in a:
                b = i.split('=')    # 每个参数再按等号分隔
                if len(b) > 1:
                    params[b[0]] = '='.join(b[1:])  #带=号的参数作为字典传入
                else:
                    params['arg%s' %(a.index(i)+100)] = i
        if kwargs:
            params = dict(params.items()+kwargs.items())
        obj = urllib.urlencode(params)
        res = self.postRequest(obj)
        return res

    # master本地执行
    def saltRun(self, fun, client='runner_async', arg=None, **kwargs):
        params = {'client':client,'fun':fun}
        if arg:
            a = arg.split(',')
            for i in a:
                b = a.split('=')
                if len(b) > 1:
                    params[b[0]] = '='.join(b[1:])
                else:
                    params['arg%s' % (a.index(i) + 100)] = i
        if kwargs:
            params = dict(params.items()+kwargs.items())
        obj = urllib.urlencode(params)
        res = self.postRequest(obj)
        return res

    # 获取job id的详细执行结果
    def saltJob(self, jid=''):
        if jid:
            prefix = '/jobs/' + jid
        else:
            prefix = '/jobs'
        res = self.postRequest(None, prefix)
        return res

    # 获取grains
    def saltMinions(self, minion=''):
        if minion and minion != '*':
            prefix = '/minions/' + minion
        else:
            prefix = '/minions'
        res = self.postRequest(None, prefix)
        return res

    # 获取events
    def saltEvents(self):
        prefix = '/events'
        res = self.postRequest(None, prefix)
        return res

    # 列出keys
    def listKeys(self):
        prefix = '/keys'
        content = self.postRequest(None, prefix)
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return accepted, denied, unaccept, rejected

    # 接受key
    def acceptKey(self, key_id):
        params = {'client':'wheel','fun':'key.accept','match':key_id}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    # 删除key
    def deleteKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

