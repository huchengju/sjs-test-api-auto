# -*- coding: utf-8 -*-

class FrozenJSON1(object):

    def __new__(cls, args):
        if isinstance(args,dict):
            return object.__new__(cls)
        elif isinstance(args,list):
            return [cls(item) for item in args]
        else:
            return args

    def __init__(self,mapping):
        self.__data=dict(mapping)

    def __getattr__(self,name):
        if hasattr(self.__data,name):
            return getattr(self.__data,name)
        else:
            return FrozenJSON1(self.__data[name])

# class FrozenJSON:
#
#     def __init__(self,mapping):
#         self.__data=dict(mapping)
#     def __getattr__(self,name):
#         if hasattr(self.__data,name):
#             return getattr(self.__data,name)
#         else:
#             return FrozenJSON.build(self.__data[name])
#
#     @classmethod
#     def build(cls,obj):
#         if isinstance(obj,dict):
#             return cls(obj)
#         elif isinstance(obj,list):
#             return [cls.build(item) for item in obj]
#         else:
#             return obj

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
    f = FrozenJSON1(data)
    print(f.data.vin[0][0].data1[0][0].data3)