# -*- coding: utf-8 -*-

import json, pytest, os
from config import url as base_url, globalparam
from public.common.request import Request
from config.sjs_darp_api import url
from public.common.tools import load


class TestDarp(object):

    def setup(self):
        test_data = os.path.join(globalparam.config_file_path, "sjs_darp_api", "request.json")
        self.data = load(test_data)

    def teardown(self):
        pass

    @pytest.mark.darp_api
    @pytest.mark.api_smoke
    def test_darp_company_add(self, *args, **kwargs):

        request_url = base_url.testjavaHost + url.darp_company_add
        if args:
            request_body = json.dumps(args[0])
        else:
            request_body = json.dumps(self.data['darp_company_add']['requestdata'])
        header = self.data['darp_company_add']['header']
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.post(url=request_url, data=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('status') == 0 or response.get('statusCode') == 0
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response

    @pytest.mark.darp_api
    @pytest.mark.api_smoke
    @pytest.mark.run(order=3)
    def test_darp_admin_login(self, *args, **kwargs):

        request_url = base_url.testjavaHost + url.darp_admin_login
        if args:
            request_body = json.dumps(args[0])
        else:
            request_body = json.dumps(self.data['darp_admin_login']['requestdata'])
        header = self.data['darp_admin_login']['header']
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.post(url=request_url, data=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('code') == 200 or response.get('statusCode') == 200
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response

    @pytest.mark.darp_api
    @pytest.mark.api_smoke
    @pytest.mark.run(order=2)
    def test_drap_admin_register(self, *args, **kwargs):

        request_url = base_url.testjavaHost + url.drap_admin_register
        if args:
            request_body = json.dumps(args[0])
        else:
            request_body = json.dumps(self.data['drap_admin_register']['requestdata'])
        header = self.data['drap_admin_register']['header']
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.post(url=request_url, data=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('code') == 200 or response.get('statusCode') == 200
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response

    @pytest.mark.darp_api
    @pytest.mark.api_smoke
    @pytest.mark.run(order=1)
    def test_darp_admin_msgCode(self, *args, **kwargs):

        request_url = base_url.testjavaHost + url.darp_admin_msgCode
        if args:
            request_body = json.dumps(args[0])
        else:
            request_body = json.dumps(self.data['darp_admin_msgCode']['requestdata'])
        header = self.data['darp_admin_msgCode']['header']
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.post(url=request_url, data=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('code') == 200 or response.get('statusCode') == 200
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response



if __name__ == '__main__':

    # pytest.main(["-s",
    #              "test_sjs_darp_api.py::TestDarp::test_darp_admin_msgCode"])

    pytest.main(["-s","-m",
                 "darp_api"])
