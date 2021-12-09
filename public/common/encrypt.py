# -*- coding: utf-8 -*-

from hashlib import sha1
from hashlib import md5
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Cipher import DES
import binascii


def my_md5(msg):
    """
    md5 算法加密
    """
    hl = md5()
    hl.update(msg.encode('utf-8'))
    return hl.hexdigest()


def my_sha1(msg):
    """
    sha1 算法加密
    """
    sh = sha1()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()


def my_sha256(msg):
    """
    sha256 算法加密
    """
    sh = SHA256.new()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()


def my_des(msg, key):
    """
    DES 算法加密
    """
    de = DES.new(key, DES.MODE_ECB)
    mss = msg + (8 - (len(msg) % 8)) * '='
    text = de.encrypt(mss.encode())
    return binascii.b2a_hex(text).decode()


def my_aes_encrypt(msg, key, vi):
    """
    AES 算法的加密
    """
    obj = AES.new(key, AES.MODE_CBC, vi)
    txt = obj.encrypt(msg.encode())
    return binascii.b2a_hex(txt).decode()


def my_aes_decrypt(msg, key, vi):
    """
    AES 算法的解密
    """
    msg = binascii.a2b_hex(msg)
    obj = AES.new(key, AES.MODE_CBC, vi)
    return obj.decrypt(msg).decode()



print(my_md5('wj123456'))