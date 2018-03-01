# !/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
import time


def login():
    req = requests.session()
    url = 'https://www.zhihu.com/signup?next=%2F'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    r = req.get(url, headers=headers)
    X_Xsrftoken, X_UDID = re.findall(r'{&quot;xsrf&quot;:&quot;(.*?)&quot;,&quot;xUDID&quot;:&quot;(.*?)&quot;}', r.text)[0]

    url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'X-UDID': X_UDID,
        'X-Xsrftoken': X_Xsrftoken,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Content-Type': 'multipart/form-data'
    }
    timestamp = round(time.time(),3)
    fiels = {
        'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type': 'password',
        'timestamp': timestamp,
        'source': 'com.zhihu.web',
        'signature': '07749d2663c226c41140ce44fbdf9f19d271d7c5',
        'username': '1321742103@qq.com',
        'password': 'iL3141592653',
        'captcha': '{"img_size":[200,44],"input_points":[[70.33331298828125,15.520828247070312],[114.33331298828125,29.520828247070312]]}',
        'lang': 'cn',
        'ref_source': 'homepage',
        'utm_source': 'baidu'
    }
