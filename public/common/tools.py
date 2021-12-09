#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import ruamel.yaml

from config.globalparam import config_file_path


def load(file):
    '''
    加载yaml文件
    file: 文件路径
    return: 文件内容
    '''
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml = ruamel.yaml.YAML()
            yaml.allow_duplicate_keys = True
            data = yaml.load(f.read())
            # data = ruamel.yaml.safe_load(f.read())

        return data
    except IOError:
        print("Error: 没有找到文件或读取文件失败")


def dump(file, wriData):
    '''
    加载yaml文件
    file: 文件路径
    wriData: 写入数据
    '''
    try:
        with open(file, 'w', encoding='utf-8') as f:
            ruamel.yaml.safe_dump(wriData, f, default_flow_style=False, allow_unicode=True)
    except IOError:
        print("Error: 没有找到文件或写入文件失败")


def to_json():
    '''
    get请求时，从Charles拷贝Contents下面的Query String 参数转化为json
    :return:
    '''

    file = '{0}/params.txt'.format(config_file_path)
    t_json = {}
    with open(file, 'r', encoding='utf-8') as f:
        s = f.readlines()

    for i in s:
        t = i.split()
        if len(t) == 1:
            t.append("")
        key, value = t
        t_json[key] = value

    for key, value in t_json.items():
        if key == list(t_json.keys())[-1]:
            print("  \"{0}\": \"{1}\"".format(key, value))
        else:
            print("  \"{0}\": \"{1}\",".format(key, value))


def cut(self, num, c):
    '''
    保留c位小数  不要四舍五入
    '''
    if num:
        str_num = str(num)
        str_num = str(str_num[:str_num.index('.') + 1 + c])
    else:
        str_num = '0' + '.' + '0' * c
    return str_num


def cut_about(self, num, c):
    '''
    保留c位小数   四舍五入
    '''
    if num:
        str_num = round(num, c)
    else:
        str_num = '0' + '.' + '0' * c
    return str_num


if __name__ == '__main__':
    to_json()
