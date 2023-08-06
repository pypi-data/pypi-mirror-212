#!/usr/bin/env python
# coding:utf-8

from hashlib import md5

import requests

import sfun as util


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic_base64(self, file_path, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        base64_str = util.get_file_content_as_base64(file_path, False)
        params = {
            'codetype': codetype,
            'file_base64': base64_str
        }
        params.update(self.base_params)
        r = requests.post(
            'http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    chaojiying = Chaojiying_Client('15021869005', 'huangrui', '941459')
    imrslt = chaojiying.PostPic_base64(
        r"C:\Users\renjunfeng\Downloads\Chaojiying_Python\chaojiying_Python\a.jpg", 1902)
    print(imrslt.get("pic_str", ""))
