# -*- coding: utf-8 -*-

import pytest
import json, os
from config import globalparam,url as base_url
from public.common.connsql import MySQL
from public.common.log import Singletoncls
from public.common.request import Request
from public.common.response import Response
from public.common.tools import load
from public.common.log import Log
from config.sjs_darp_api import url

res = Response()
test_data = os.path.join(globalparam.config_file_path, "atoken_auth_api", 'request.json')
data = load(test_data)
log = Log()

@pytest.fixture(scope='class',autouse=True)
def base():
    # params = data['auth']['requestdata']
    # print("request=", base_url.testjavaHost, params)
    # response = Request.get(url=base_url.testjavaHost + url.auth, params=params, headers=base_url.header, verify=False)
    # print("response=", response)
    # try:
    #     assert response.get('status') == 0 or response.get('statusCode') == 0
    # except RuntimeError:
    #     log.error('接口请求失败!!!')
    # else:
    #     Authorization = res.get_single(response, 'data')
    #     base_url.header['Authorization'] = Authorization
    #     return response

    pass
