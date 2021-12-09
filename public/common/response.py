# -*- coding: utf-8 -*-

import ast


class Response(object):

    def __init__(self):
        pass

    # 获取结果列表
    def get_list(self, arg, arg1):

        l = []
        for key in arg:
            values = arg[key]
            if arg1 == key:
                l.append(values)

        for key in arg:

            if isinstance(arg[key], list):
                for v in arg[key]:
                    if isinstance(v, dict):
                        res = self.get_list(v, arg1)
                        for x in res:
                            l.append(x)
                    if isinstance(v, list):
                        for j in v:
                            res = self.get_list(j, arg1)
                            for x in res:
                                l.append(x)


            elif isinstance(arg[key], dict):
                res1 = self.get_list(arg[key], arg1)
                for y in res1:
                    l.append(y)

        return l

    # 获取单个结果值
    def get_single(self, str1, str2):

        for key in str1:
            if key == str2:
                return str1[key]

        for key in str1:
            if isinstance(str1[key], list):
                for i in str1[key]:
                    if isinstance(i, dict):
                        return self.get_single(i, str2)
                    if isinstance(i, list):
                        for j in i:
                            return self.get_single(j, str2)

            elif isinstance(str1[key], dict):
                return self.get_single(str1[key], str2)

    def getValue(self, dic1, keys):
        global res
        if isinstance(dic1, dict):
            for key in dic1:
                if key == keys:
                    temp_value = dic1[key]
                    return temp_value
                elif isinstance(dic1[key], dict):
                    res = self.get_single(dic1[key], keys)
                elif isinstance(dic1[key], list):
                    for i in dic1[key]:
                        if isinstance(i, dict):
                            res = self.get_single(i, keys)
                else:
                    continue
                if res == None:
                    continue
                else:
                    return res


        elif not isinstance(dic1, dict):
            dic1 = ast.literal_eval(dic1)
            return self.get_single(dic1, keys)

    def getValist(self, dic1, keys):

        l = []

        if isinstance(dic1, dict):

            for key in dic1:
                if key == keys:
                    temp_value = dic1[key]
                    return temp_value

                elif isinstance(dic1[key], dict):
                    res = self.get_list(dic1[key], keys)
                elif isinstance(dic1[key], list):
                    for i in dic1[key]:
                        if isinstance(i, dict):
                            res = self.get_list(i, keys)
                            l.append(res[0])
                else:
                    continue
                if l == None:
                    continue
                else:
                    return l

        elif not isinstance(dic1, dict):
            dic1 = ast.literal_eval(dic1)
            return self.get_list(dic1, keys)


if __name__ == '__main__':
    data = {'data': {'action_name': '', 'amount': '1', 'block_hash': '', 'block_height': '10197745', 'block_num': '',
                     'block_state': '', 'btc_amount': '', 'build_coin_type': '', 'build_value': '', 'code': '',
                     'comment': '', 'confirm': '', 'confirm_time': '38079', 'contract_addr': '', 'cpu_quantity': '',
                     'create_time': '', 'decimals': '', 'fee': '0.00021',
                     'from': '0xd5d0a96adafcaffdb32593b05194e522ba1a0cd4', 'from_addr': '', 'gas_limit': '21000',
                     'gas_price': '10', 'gas_used': '21000', 'id': '', 'in_out': '', 'is_equal_to': 'True',
                     'is_success': '1', 'mark_state': '', 'memo': '', 'minimum_tx_hash': '', 'net_quantity': '',
                     'nonce': '1', 'pending_tx_count': '0', 'plat_type': '', 'producers': '', 'proxy': '',
                     'push_time': '', 'quantity': '', 'ram_bytes': '', 's': '1', 'shift': '', 'size': '', 'symbol': '',
                     'timestamp': '1587025301', 'title': '', 'to': '0x076f83c7d56cd6174f5a1d10283b2dc9558e1924',
                     'to_addr': '', 'tran_rate': '',
                     'tx_hash': '0x7a94f9f1d7a4f62ddcc5a0afc4e5488553d62c1f2bfd0afd392d28ecbdf9e029', 'tx_state': '1',
                     'tx_status': '', 'tx_time': '', 'tx_type': '', 'type': '', 'unconfirmed_minimum_nonce': '',
                     'vin': [[{'data1': [[{'data3': 'hihi'}]]}]], 'vout': []},
            'extend': {'contract_addr': '', 'decimals': '', 'error': '', 'input_raw': '',
                       'the_current_height': 10235824, 'to_confirm_the_number': 30, 'token_amount': '',
                       'token_name': '', 'type': 60}, 'msg': '', 'status': 0}
    r = Response()
    res = r.getValue(data, 'the_current_height')
    print(res)
