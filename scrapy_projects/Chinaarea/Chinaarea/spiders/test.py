# !/usr/bin/python3
# -*- coding: utf-8 -*-

import requests


url = 'https://www.aqistudy.cn/api/historyapi.php'
data = {
    'hd': ''
}

r = requests.post(url)
print(r.text)