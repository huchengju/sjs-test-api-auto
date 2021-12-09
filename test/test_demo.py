#/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def test_doc():

    r = requests.get("http://10.101.12.15:8091/darp/doc.html")
    print(r.json())


if __name__ == '__main__':

    test_doc()


