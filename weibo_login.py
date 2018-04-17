# !/usr/bin/python3
# -*- coding:utf-8 -*- 

import time
import urllib3
import json
import re
import requests
import base64
from urllib import parse
import rsa
import binascii


class WeiBo(object):
    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        urllib3.disable_warnings()

    def get_server_data(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php'
        params = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.get_su(),
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.19)',
            '_': str(int(time.time() * 1000)),
        }
        r = self.session.get(url=url, params=params, headers=self.headers, verify=False)
        r.encoding = r.apparent_encoding
        data = re.findall(r'sinaSSOController\.preloginCallBack\((.*?)\)', r.text)[0]
        self.server_data = json.loads(data)

    def login(self):
        self.get_server_data()
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'vsnf': '1',
            'su': self.get_su(),
            'service': 'miniblog',
            'servertime': self.server_data['servertime'],
            'nonce': self.server_data['nonce'],
            'pwencode': 'rsa2',
            'rsakv': self.server_data['rsakv'],
            'sp': self.get_sp(),
            'sr': '1280*720',
            'encoding': 'UTF-8',
            'prelt': '59',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }
        # post请求获得第一个跳转url
        r1 = self.session.post(url=url, headers=self.headers, data=data, verify=False)
        r1.encoding = r1.apparent_encoding
        refresh_url = re.findall('location\.replace\("(.*?)"\);', r1.text)[0]

        # 获得第二个跳转url
        r2 = self.session.get(url=refresh_url, headers=self.headers, verify=False)
        r2.encoding = r2.apparent_encoding
        skip_url = re.findall(r"location\.replace\('(.*?)'\);", r2.text)[0]

        r3 = self.session.get(url=skip_url, headers=self.headers, verify=False)
        r3.encoding = r3.apparent_encoding
        args = re.search(r'userinfo":{"uniqueid":"(?P<uniqueid>.*?)","userid":null,"displayname":null,"userdomain":"\?wvr=(?P<wvr>.*?)&lf=(?P<lf>.*?)"}', r3.text)

        url = 'https://weibo.com/u/{}/home?wvr={}&lf={}'.format(args.group('uniqueid'),
                                                                args.group('wvr'),
                                                                args.group('lf'),
                                                                )
        r4 = self.session.get(url=url, headers=self.headers, verify=False)
        r4.encoding = 'utf8'
        print(r4.text)

    def get_su(self):
        user_quote = parse.quote(self.username)
        user_base64 = base64.b64encode(user_quote.encode('utf8'))
        return user_base64

    def get_sp(self):
        message = str(self.server_data['servertime']) + '\t' + self.server_data['nonce'] + '\n' + str(self.password)
        public_key = rsa.PublicKey(int(self.server_data['pubkey'], 16), int('10001', 16))
        sp_ = rsa.encrypt(message=message.encode('utf8'), pub_key=public_key)
        sp = binascii.b2a_hex(sp_)
        return sp


if __name__ == '__main__':
    weibo = WeiBo('18163910296', '1419814355')
    weibo.login()
