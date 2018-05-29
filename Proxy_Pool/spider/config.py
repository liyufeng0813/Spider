# !/usr/bin/python3
# -*- coding:utf-8 -*-

import random


def get_page(scope, count):
    if not isinstance(scope, tuple) and not isinstance(count, int):
        return []

    page_set = set()
    while len(page_set) != count:
        page_set.add(random.randrange(*scope))

    return list(page_set)


User_Agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'User-Agent:Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': random.choice(User_Agent),
}

parser_message_list = [
    # {
    #     'url_list': ['https://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 10)],
    #     'type': 'xpath',
    #     'pattern': '//div[@id="list"]/table/tbody/tr',
    #     'position': {'ip': './td[1]', 'port': './td[2]'},
    # },
    {
        'url_list': ['http://www.xicidaili.com/nn/{}'.format(page) for page in get_page((1, 150), 4)],
        'type': 'xpath',
        'pattern': '//table[@id="ip_list"]/tr[position()>1]',
        'position': {'ip': './td[2]', 'port': './td[3]'},
    }
]
