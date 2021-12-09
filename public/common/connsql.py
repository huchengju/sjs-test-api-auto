# -*- coding: utf-8 -*-

import threading
import pymysql

from config.globalparam import server_path
from public.common.tools import load


class MySQL(object):
    _instance_lock = threading.Lock()

    def __init__(self):

        self.db_data = load(server_path)['Sql']
        self.db = pymysql.connect(host=self.db_data['ip'], user=self.db_data['username'], password=self.db_data['password'])
        self.db.autocommit(True)
        self.cursor = self.db.cursor()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MySQL, "_instance"):
            with MySQL._instance_lock:
                if not hasattr(MySQL, "_instance"):
                    MySQL._instance = object.__new__(cls, *args, **kwargs)

        return MySQL._instance

    def reConnect(self):

        try:
            self.db.ping()
        except:
            self.db = pymysql.connect(host=self.db_data['ip'], user=self.db_data['user'], password=self.db_data['passwd'])
            self.cursor = self.db.cursor()

    def fetchOne(self, sql):
        try:
            self.cursor.execute(sql)
            # print(self.cursor.execute(sql))
            self.data = self.cursor.fetchone()
            return self.data
        except:
            raise Exception("Error: unable to fetch data")

    def fetchAll(self, sql):
        try:
            self.cursor.execute(sql)
            self.data = self.cursor.fetchall()
            return self.data
        except:
            raise Exception("Error: unable to fetch data")

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


if __name__ == "__main__":

    q = MySQL()
    res = q.fetchOne("select order_num from atoken_defi.df_otc_order where wallet_id = '9b2b3ec9c642e4910ba842f44e5d4f707fae2f989ccec63fcaf6df93bf2cbbb2' "
               "and order_type = 2 order by id desc limit 1")

    print(res)