# !/usr/bin/python3
# -*- coding:utf-8 -*- 

import time
import random
import urllib3

import requests

from spider import config


class Downloader(object):
    def __init__(self):
        urllib3.disable_warnings()
        self.session = requests.session()

    def get_html(self, url):
        headers = config.headers
        try:
            response = self.session.get(url, headers=headers, timeout=7, verify=False)
        except Exception:
            return ''

        response.encoding = response.apparent_encoding
        if response.status_code != 200:
            raise ConnectionError
        return response.text

    def download_html(self, url):
        try:
            html = self.get_html(url)
            return html
        except BaseException:
            count = 1
            while count <= 3:
                try:
                    time.sleep(random.randrange(2, 3))
                    html = self.get_html(url)
                except BaseException:
                    count += 1
                else:
                    return html
            return ''


if __name__ == '__main__':
    url_list = ['https://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 10)]
    downloader = Downloader()
    html_list = []
    for url in url_list:
        html = downloader.download_html(url)
        html_list.append(html)
        print(html)
    print(len(html_list))
