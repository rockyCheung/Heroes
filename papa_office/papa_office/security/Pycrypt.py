# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
# from binascii import b2a_hex, a2b_hex
import base64

class Pycrypt(object):
    def __init__(self,key,salt):
        self.key = key
        self.mode = AES.MODE_CBC
        self.salt = salt

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        text = text+'@'+self.salt
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        # return b2a_hex(self.ciphertext)
        return base64.encodestring(ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plainText = cryptor.decrypt(base64.decodestring(text))
        plainText = plainText.rstrip('\0')
        return plainText.partition('@')[0]

# c = Pycrypt('1234567812345678','salt')
# e = c.encrypt('123')
# d = c.decrypt(e)
# print e,d