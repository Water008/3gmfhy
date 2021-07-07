#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print('请安装加解密库pycryptodome')


class AesSample(object):
    def __init__(self):
        self.key = 'greenh5java12345'.encode('utf-8')
        self.iv = 'greenh5java12345'.encode('utf-8')
        self.mode = AES.MODE_CBC

    def encode(self, data):
        cipher = AES.new(self.key, self.mode, self.iv)
        pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
        result = base64.encodebytes(cipher.encrypt(pad_pkcs7))
        encrypted_text = str(result, encoding='utf-8').replace('\n', '')
        return encrypted_text

    def decode(self, data):
        cipher = AES.new(self.key, self.mode, self.iv)
        base64_decrypted = base64.decodebytes(data.encode('utf-8'))
        una_pkcs7 = unpad(cipher.decrypt(base64_decrypted), AES.block_size, style='pkcs7')
        decrypted_text = str(una_pkcs7, encoding='utf-8')
        return decrypted_text

    def test(self):
        data1 = '12345678'
        data2 = 'XjrFNon4uyNqVIufmsD3dA=='
        print('加密结果：', self.encode(data1))
        print('解密结果：', self.decode(data2))


if __name__ == '__main__':
    blog = AesSample()
    blog.test()