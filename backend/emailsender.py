#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

user = "**********@qq.com"
pwd = "**********"
to = ["**********@139.com","***********@qq.com"]
msg = MIMEMultipart()
msg['Subject'] = '这里是主题。。。'
content1 = MIMEText('这里是正文。。。', 'plain', 'utf-8')
msg.attach(content1)
attfile = 'C:\\Users\\yezl\\Desktop\\test.txt'
basename = os.path.basename(attfile)
fp = open(attfile,'rb')
att = MIMEText(fp.read(),'base64','utf-8')
att['Content-Type'] = 'application/octet-stream'
att.add_header('Content-Disposition','attachment',filename=('gbk','',basename))
encoders.encode_base64(att)
msg.attach(att)
# -------------------------------------------
s = smtplib.SMTP_SSL('smtp.qq.com')
s.login(user,pwd)
s.sendmail(user,to,msg.as_string())
print '发送成功'
s.close()
fp.close()