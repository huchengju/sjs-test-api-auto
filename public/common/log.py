#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
from functools import wraps

from public.common.logger import Log
import time


def log(func):
    ''' 打印log装饰器，不带参数'''
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            # print("current func:",func.__name__)
            Log().info("current func: %s" % func.__name__)
            return func(*args, **kwargs)
        except Exception as e:
            Log().error("{%s} is error,here are details: %s" % (func.__name__, traceback.format_exc()))

    return inner


def Singleton(cls):
    ''' 单例 '''
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton()


class Singletoncls(object):
    ''' 单例 '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singletoncls, cls).__new__(cls, *args, **kwargs)
        return cls._instance

def reqTime(func):
    '''
        请求响应时间装饰器
    '''
    @wraps(func)
    def inner(*args, **kwargs):

        startTime = time.time()
        res = func(*args, **kwargs)
        endTime = time.time()
        message = "current Function: [{0}], run time is {1}".format(func.__name__, format(endTime - startTime, '.2f'))
        Log().info(message)
        return res

    return inner
