#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest

from config import globalparam, url
from public.common.logger import Log
from public.common.request import Request
from public.common.tools import load

config = load(globalparam.server_path)['Email']

# 测试报告的路径
reportPath = globalparam.report_path
# 配置收发件人
recvaddress = ''
config['TO']
sendaddr_name = config['user']
sendaddr_pswd = config['password']
log = Log()


class SendMail:

    def __init__(self, recver=None):
        """接收邮件的人：list or tuple"""
        if recver is None:
            self.sendTo = recvaddress
        else:
            self.sendTo = recver

    def __get_report(self):
        """获取最新测试报告"""
        dirs = os.listdir(reportPath)
        dirs.sort()
        newreportname = dirs[-1]
        print('The new report name: {0}'.format(newreportname))
        return newreportname

    def send_mail(self):
        # --------- 读取config.ini配置文件 ---------------
        HOST = config["HOST_SERVER"]
        PORT = config["HOST_PORT"]
        SENDER = config["FROM"]
        RECEIVER = config["TO"]
        USER = config["user"]
        PWD = config["password"]
        SUBJECT = config["SUBJECT"]
        msg = MIMEMultipart()

        """生成邮件的内容，和html报告附件"""
        newreport = self.__get_report()
        self.msg = MIMEMultipart()
        self.msg['Subject'] = config['SUBJECT']
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        with open(os.path.join(reportPath, newreport), 'rb') as f:
            mailbody = f.read()
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
        self.msg.attach(html)

        msgtext = MIMEText(mailbody, 'html', 'utf-8')
        msg.attach(msgtext)  # 邮件正文内容

        msg['from'] = SENDER
        msg['to'] = RECEIVER
        msg['Subject'] = Header(SUBJECT, 'utf-8')

        with open(os.path.join(reportPath, newreport), 'rb') as f:
            attfile = f.read()
        att = MIMEText(attfile, 'base64', 'utf-8')

        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="Atoken_Api_testresult.html"'
        msg.attach(att)
        try:
            server = smtplib.SMTP_SSL(HOST, PORT)
            server.login(USER, PWD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
            log.info("邮件发送成功！")
        except Exception as  e:
            log.warning("失败: " + str(e))
        finally:
            server.quit()  # 关闭连接

    @pytest.mark.smoke
    def send_report(self, env, report_url):

        isAtAll = True
        ddMessage = {
            "at": {
                "isAtAll": isAtAll,
                "atMobiles": [

                ]
            },
            "text": {
                "content": "[" + env + "]测试报告:" + report_url
            },
            "msgtype": "text"
        }
        response = Request.post(url=url.dingding, data=json.dumps(ddMessage), headers=url.header, verify=False)
        print("response=", response)


if __name__ == '__main__':
    sendMail = SendMail()
    # sendMail.send_mail()
    # sendMail.send_report("test", "http://springboot.biliangwang.com/#/applications")
    report_name = time.strftime("%Y%m", time.localtime()) + "/" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    report_url = url.report % report_name
    print(report_url)
