import os
import re

from requests import Session
from string import Template
from config.globalparam import base_path,config_file_path
from public.common.tools import dump,load
import json
from public.common.response import Response
from public.common.log import Log
import re

template = Template("""
${api} = "${apiname}"
""")

jason_template = Template("""
    "${apifunc}": {
        "methodtype": "${methodtype}",
        "header": ${header},
        "requestdata": ${requestparams}
    },
        
""")

method_post_template = Template('''
    
    @pytest.mark.api_smoke
    def test_${case_name}(self, *args, **kwargs):
        request_url = base_url.testjavaHost + url.${case_name}
        if args:
            request_body = json.dumps(args[0])
        else:
            request_body = json.dumps(${method_request})
        header = ${method_header}
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.${method_type}(url=request_url, data=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('status') == 0 or response.get('statusCode') == 0
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response
            
    ''')

method_get_template = Template('''
    
    @pytest.mark.api_smoke
    def test_${case_name}(self, *args, **kwargs):
        request_url = base_url.testjavaHost + url.${case_name}
        if args:
            request_body = args[0]
        else:
            request_body = ${method_request}
        header = ${method_header}
        headers = base_url.header
        headers.update(header)
        print("request=", request_url, request_body)
        response = Request.${method_type}(url=request_url, params=request_body, headers=headers, verify=False)
        print("response=", response)
        try:
            assert response.get('status') == 0 or response.get('statusCode') == 0
        except RuntimeError:
            print('接口请求失败!!!')
        else:
            return response
            
    ''')

file_template = Template('''# -*- coding: UTF-8 -*-
import json
import pytest
import os
from config import url as base_url, globalparam
from public.common.request import Request
from public.common.response import Response
from config.${service_name} import url
from public.common.tools import load


class Test${class_name}(object):

    def setup(self):
        test_data = os.path.join(globalparam.config_file_path, "${service_name}", 'request.json')
        self.data = load(test_data)

    def teardown(self):
        pass

    ''')

def parse_api(k,prefix=None):

    api = re.sub(r"[/-]", "_", k)
    api = api[1::]
    if prefix:
        api = prefix + api
    if api.startswith("{"):
        api = re.sub(r"\_?\{.*?\}\_?", "", api)
    elif api.endswith("}"):
        api = re.sub(r"\_?\{.*?\}", "", api)
    else:
        api = re.sub(r"\{.*?\}\_?", "", api)

    if not api.startswith("inner_") and not api.startswith("admin_"):
        return api
    else:
        return None

def replace_data(file_name, old_data=None, new_data=None ):

    f = open(file_name, 'r')
    new_f = "{0}.bak".format(file_name)
    new_file = open(new_f, 'w')

    if old_data:

        for line in f.readlines():
            new_file.write(line.replace(old_data, new_data))
        f.close()

    else:
        d_lines = f.readlines()
        for line in d_lines:
            if d_lines.index(line) == len(d_lines) -1:
                new_file.write(line.replace(line, ''))
            else:
                new_file.write(line)
    f.close()
    new_file.close()
    os.remove(file_name)
    os.rename(new_f, file_name)

def write_template(template_name, file_name):

    with open(file_name, 'a') as f:
        f.write(template_name)
        f.close()

def parse_json(key, val, definitions):

    method_type = key
    request_param = val.get('parameters')
    hea, req = {},{}
    p_data = ""
    if request_param:
        if method_type == 'get':
            for i in request_param:
                if i.get('in', None) == 'header':
                    header = i.get('name', None)
                    h = {"{}".format(header): ""}
                    hea.update(h)
                else:
                    val = i.get('name', None)
                    val = val.replace('{', '').replace('}', '')
                    v = {"{}".format(val): ""}
                    req.update(v)

        elif method_type == 'post':
            for i in request_param:
                if i.get('in', None) == 'header':
                    header = i.get('name', None)
                    h = {"{}".format(header): ""}
                    hea.update(h)
                else:
                    val = i.get('name', None)
                    val = val.replace('{', '').replace('}', '')
                    v = {"{}".format(val): ""}
                    req.update(v)

                schema = i.get('schema', None)
                if schema:
                    defin = schema.get('$ref')
                    if defin:
                        defin = defin.split('/')[2]
                        if definitions:
                            for k, v in definitions.items():
                                if defin == k:
                                    p_data = v.get('properties')
                                    for k, v in p_data.items():
                                        p_data[k] = ""
    return hea, req, p_data

def parse_func(ser_name, c_name, url, data_json):



    try:

        imp = 'from public.base.{0} import {1}'.format(ser_name, c_name)
        exec(imp)
        g = '{0}.setup'.format(c_name)
        eval(g)
        if not url.startswith('#'):
            if url.strip() != '':
                i = url.strip().split('=')
                func_name = i[0].strip()
                for k, v in data_json.items():
                    f_name = 'test_{0}'.format(func_name)
                    f = "hasattr({0}, '{1}')".format(c_name, f_name)
                    fo = eval(f)
                    if func_name == k and fo == False:
                        method_type = v['methodtype']
                        params = "self.data['{}']['requestdata']".format(k)
                        header = "self.data['{}']['header']".format(k)

                        return method_type, func_name, params, header

    except Exception as e:
        return e

class Generator(object):

    def __init__(self, swagger_url, service_name):

        self.log = Log()
        self.project_name = service_name
        res = Session().request('get', swagger_url).json()
        self.data = res.get('paths', None)
        self.definitions = res.get('definitions', None)

        # base 目录下 创建存放测试 case 的文件
        self.case_py = os.path.join(base_path, 'test_{}.py'.format(self.project_name))
        if not os.path.isfile(self.case_py):
            with open(self.case_py, mode="w", encoding="utf-8") as f:
                f.close()

        # config 目录下，创建以 service_name 命名的文件夹
        self.service_path = os.path.join(config_file_path, self.project_name)
        if not os.path.isdir(self.service_path):
            os.makedirs(self.service_path)

        # 创建存放接口url的文件
        self.url_py = os.path.join(self.service_path, 'url.py')

        # 创建存放配置文件的文件
        self.request_json = os.path.join(self.service_path, 'request.json')

        if not os.path.isfile(self.url_py):
            with open(self.url_py, 'w') as f:
                f.write("# -*- coding: utf-8 -*- \n")
                f.close()

        if not os.path.isfile(self.request_json):
            with open(self.request_json, mode="w", encoding="utf-8") as f:
                f.write('')
                f.close()


    def generator_url(self, prefix=None):

        # 读取数据
        imp = 'from config.{0} import url'.format(self.project_name)
        exec(imp)
        for k, v in self.data.items():
            
            if parse_api(k):
                api = parse_api(k)
                # 判断接口是否实现了get/post 方法
                if len(v) > 1:
                    api_get = api + '_get'
                    try:
                        # 判断是否接口已经存在
                        g = 'url.{0}'.format(api_get)
                        val = eval(g)
                        # if val == k: # 如果存在且未有改变，忽略；如果存在有变化，重新写入
                        #    pass
                        # else:
                        #     content_in_file = '{0} = "{1}"'.format(api_get, val)
                        #     if prefix:
                        #         k = prefix + k
                        #     new_content = '{0} = "{1}"'.format(api_get, k)
                        #     replace_data(self.url_py, content_in_file, new_content)

                    except AttributeError:
                        if prefix:
                            k = prefix + k
                        url_template = template.substitute(apiname=k, api=api_get)
                        write_template(url_template, self.url_py)

                    api_post = api + '_post'
                    try:
                        g = 'url.{0}'.format(api_post)
                        val = eval(g)
                        # if val == k:
                        #     pass
                        # else:
                        #     content_in_file = '{0} = "{1}"'.format(api_get, val)
                        #     k = prefix + k
                        #     new_content = '{0} = "{1}"'.format(api_get, k)
                        #     replace_data(self.url_py, content_in_file, new_content)

                    except AttributeError:
                        if prefix:
                            k = prefix + k
                        url_template = template.substitute(apiname=k, api=api_post)
                        write_template(url_template, self.url_py)
                else:
                    try:
                        g = 'url.{0}'.format(api)
                        val = eval(g)
                        # if val == k:
                        #     pass
                        # else:
                        #     content_in_file = '{0} = "{1}"'.format(api, val)
                        #     if prefix:
                        #         k = prefix + k
                        #     new_content = '{0} = "{1}"'.format(api, k)
                        #     replace_data(self.url_py, content_in_file, new_content)

                    except AttributeError:
                        if prefix:
                            k = prefix + k
                        url_template = template.substitute(apiname=k, api=api)
                        write_template(url_template, self.url_py)

    def generator_json(self):

        req_data = load(self.request_json)
        # 判断json数据是否存在
        if not req_data:
            with open(self.request_json, mode="w", encoding="utf-8") as f:
                f.write('{')
                f.close()

        for k, v in self.data.items():

            if parse_api(k):
                api = parse_api(k)
                api_get, api_post = None, None

                if len(v) > 1:
                    api_get = api + '_get'
                    api_post = api + '_post'

                for key, val in v.items():

                    method_type = key
                    if method_type == "get":
                        hea, req, p_data = parse_json(key, val, self.definitions)
                        if req_data:
                            l_keys = dict(req_data).keys()
                            if api_get and api_get not in l_keys:
                                json_temp = jason_template.substitute(apifunc=api_get, methodtype=method_type,
                                                                      header=json.dumps(hea), requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)
                            elif api_get == None and api not in l_keys:
                                json_temp = jason_template.substitute(apifunc=api, methodtype=method_type,
                                                                      header=json.dumps(hea), requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)

                        else:
                            if api_get:
                                json_temp = jason_template.substitute(apifunc=api_get, methodtype=method_type,
                                                                      header=json.dumps(hea),
                                                                      requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)
                            else:
                                json_temp = jason_template.substitute(apifunc=api, methodtype=method_type,
                                                                      header=json.dumps(hea),
                                                                      requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)

                    elif method_type == 'post':

                        hea, req, p_data = parse_json(key, val, self.definitions)
                        if req_data:
                            l_keys = dict(req_data).keys()
                            if api_post and api_post not in l_keys:
                                json_temp = jason_template.substitute(apifunc=api_post, methodtype=method_type,
                                                                      header=json.dumps(hea), requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)

                            elif api_post == None and api not in l_keys:
                                json_temp = jason_template.substitute(apifunc=api, methodtype=str(method_type),
                                                                      header=json.dumps(hea),
                                                                      requestparams=json.dumps(p_data))
                                write_template(json_temp, self.request_json)
                        else:
                            if api_post:
                                json_temp = jason_template.substitute(apifunc=api_post, methodtype=method_type,
                                                                      header=json.dumps(hea), requestparams=json.dumps(req))
                                write_template(json_temp, self.request_json)
                            else:
                                json_temp = jason_template.substitute(apifunc=api, methodtype=str(method_type),
                                                                      header=json.dumps(hea),
                                                                      requestparams=json.dumps(p_data))
                                write_template(json_temp, self.request_json)

        if not req_data:
            with open(self.request_json, mode="a", encoding="utf-8") as f:
                f.write('}')
                f.close()

    def generator_func(self):

        case_name = self.project_name.split('_')
        if len(case_name) >= 2:
            case_name = case_name[1]

        ser_name = 'test_{0}'.format(self.project_name)
        c_name = 'Test{0}'.format(case_name)

        try:

            with open(self.url_py, 'r') as f:
                data_url = f.readlines()
                f.close()
            data_json = load(self.request_json)

            for i in data_url:
                if parse_func(ser_name, c_name, i, data_json):
                    method_type, func_name, params, header = parse_func(ser_name, c_name, i, data_json)
                    if method_type == 'post':
                        post_temp = method_post_template.substitute(case_name=func_name,
                                                                    method_request=params,
                                                                    method_type=method_type,
                                                                    method_header=header,
                                                                    method_response_status=0
                                                                    )
                        write_template(post_temp, self.case_py)

                    elif method_type == 'get':
                        post_temp = method_get_template.substitute(case_name=func_name,
                                                                   method_request=params,
                                                                   method_type=method_type,
                                                                   method_header=header,
                                                                   method_response_status=0
                                                                   )
                        write_template(post_temp, self.case_py)

        except :

            case_temp = file_template.substitute(class_name=case_name, service_name=self.project_name, json_path=self.request_json)
            write_template(case_temp, self.case_py)

            with open(self.url_py, 'r') as f:
                data_url = f.readlines()
                f.close()
            data_json = load(self.request_json)

            for i in data_url:
                if parse_func(ser_name, c_name, i, data_json):
                    method_type, func_name, params, header = parse_func(ser_name, c_name, i, data_json)

                    if method_type == 'post':
                        post_temp = method_post_template.substitute(case_name=func_name,
                                                                    method_request=params,
                                                                    method_type=method_type,
                                                                    method_header=header,
                                                                    method_response_status=0
                                                                    )
                        write_template(post_temp, self.case_py)

                    elif method_type == 'get':
                        post_temp = method_get_template.substitute(case_name=func_name,
                                                                   method_request=params,
                                                                   method_type=method_type,
                                                                   method_header=header,
                                                                   method_response_status=0
                                                                   )
                        write_template(post_temp, self.case_py)



if __name__ == "__main__":
    print("------generator from swagger------")
    # g = Generator("http://172.17.3.99:15030/v2/api-docs", "atoken_activity_service")
    # Generator("http://172.17.3.123:15100/v2/api-docs", "atoken_lighning_api")
    # Generator("http://172.17.3.218:15201/v2/api-docs", "atoken_defi_api")
    # g = Generator("http://172.17.3.123:15070/v2/api-docs", "atoken_core_api")
    # Generator("http://172.17.3.99:20001/v2/api-docs", "atoken_nyar_service")
    # g = Generator("http://172.17.3.99:15150/v2/api-docs", "atoken_activity_api")
    # Generator("http://172.17.3.99:15030/v2/api-docs", "atoken_activity_service")
    # g = Generator("http://172.17.3.99:15090/v2/api-docs", "atoken_auth_api")
    # g = Generator("http://172.17.3.99:16002/v2/api-docs", "atoken_foundation_api")
    g = Generator("http://10.101.12.15:8091/darp/doc.html", "sjs_darp_api")
    g.generator_url()
    # g.generator_json()
    # g.generator_func()



