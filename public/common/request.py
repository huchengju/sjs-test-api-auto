# -*- coding: utf-8 -*-

import requests


class Request():

    def __init__(self):
        pass

    @staticmethod
    def get(*args, **kwargs):
        r = requests.get(*args, **kwargs)
        if r.status_code == 200:
            try:
                response = r.json()
                return response
            except:
                response = r.text
                return response
        else:
            # raise Exception("Request Error,status_code = %s" %(r.status_code))
            return r.status_code

    @staticmethod
    def post(*args, **kwargs):
        r = requests.post(*args, **kwargs)
        if r.status_code == 200 or 201:
            try:
                response = r.json()
                return response
            except:
                response = r.text
                return response
        else:
            # raise Exception("Request Error,status_code = %s" %(r.status_code))
            return r.status_code

    @staticmethod
    def put(*args, **kwargs):
        r = requests.put(*args, **kwargs)
        if r.status_code == 200:
            try:
                response = r.json()
                return response
            except:
                response = r.text
                return response
        else:
            # raise Exception("Request Error,status_code = %s" %(r.status_code))
            return r.status_code
