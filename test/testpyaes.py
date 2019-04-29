
import os
import pyaes
import base64
key = "This_key_for_demo_purposes_only!"

s = os.urandom(32)
# print(str(s))
# base64code = base64.encodebytes(s)
# print(base64code)
# print(base64.decodebytes(base64code))
# 
# b=b'\xed6j\xd7_\xbd^\xbf9\xf9\xda\x8aY=\xd8+0\xe7\xb2\xdb4n\xa0\xe9\xf1\xd1\xb1\x8d\xc4c\xf0\xc7'
# string=str(b,'utf-8')
# print(string)
# aes = pyaes.AESModeOfOperationCTR(s)

aes = pyaes.AESModeOfOperationCTR(s)
plaintext = "Text may be any length you wish, no padding is required"
ciphertext = aes.encrypt(plaintext)

name  = 'rocky'
by = name.encode('utf-8')
print(ciphertext)
aa = aes.encrypt(name)
print(aes.decrypt(ciphertext))