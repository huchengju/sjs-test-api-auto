#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os
from locust import task, HttpUser, TaskSet
import queue

class UserBehavior(TaskSet):

    def on_start(self):
        print('start')

    @task
    def test_creteorder(self):

        url = '/ccm/orders'
        addr = self.user.queue_data.get()
        print(addr)
        header = {'Content-Type': 'application/json; charset=utf-8'}
        proxy = {'http': '192.168.115.50:8888'}
        data = {
                "addr": "{0}".format(addr),
                "goodsId": 1,
                "coinName": "FIL",
                "amount": 300,
                "profitAddr": "12345678901234567890",
                "price": 300,
                "quantity": 1,
                "paymentType": "USDT(ERC20)"
        }
        # r = self.client.post(url=url,data=json.dumps(data), headers=header, proxies=proxy)
        r = self.client.post(url=url,data=json.dumps(data), headers=header)
        print(r.json())

class WebsiteUser(HttpUser):
    host = "http://172.17.3.123:15010"
    tasks = [UserBehavior]
    address = ['0xBCb3E4407D149F26e2Ee3938FAFF523E343FB974','0xdeb5cfb86ab2a4b2e568f0e3e562c9576fe9d85f','0x7b1ebf251a410ecfc4d62707bfab937a285dfa1e','0x8b8943de75091258bbbd94a0c118c980e05895b2',
        '0x0b76532e22713f33ea94b05373a2fd898d7ed89a','0xea8934c294aab299fff4773f4ddb0e08d51e16a8','0x076f83c7d56cd6174f5a1d10283b2dc9558e1924']
    queue_data = queue.Queue()
    for i in range(100,1000):
        address = '0xBCb3E4407D149F26e2Ee3938FAFF523E343FB{0}'.format(i)
        queue_data.put_nowait(address)

    min_wait = 1500
    max_wait = 5000


if __name__ == '__main__':
    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    os.system("locust -f performancetest.py")