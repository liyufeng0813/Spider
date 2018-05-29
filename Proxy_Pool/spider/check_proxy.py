# !/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import urllib3
from multiprocessing.pool import ThreadPool
import math

import requests
import gevent
from gevent import monkey; monkey.patch_socket()

from spider import config
from db.mongo_helper import MongoHelper


urllib3.disable_warnings()


def check_proxy_func(proxies, proxy_dict, queue_valid):
    """
    检测代理IP地址，把可用的代理IP添加到队列中
    """
    start_time = time.time()
    try:
        url = 'http://httpbin.org/ip'
        response = requests.get(url, headers=config.headers, verify=False, proxies=proxies, timeout=10)
        if response.status_code == 200:
            speed = time.time() - start_time
            proxy_dict['speed'] = round(speed, 1)
            print('代理 {} 可用，响应时间：{}'.format(proxies, speed))
            queue_valid.put(proxy_dict)
    except Exception:
        pass


def check_proxy(queue_all, queue_valid):
    """
    从queue_all队列中取值进行检测，通过多线程提高检测代理IP的速度。
    """
    pool = ThreadPool(16)
    while not queue_all.empty():
        proxy_dict = queue_all.get()
        proxies = {'http': 'http://{}:{}'.format(proxy_dict['ip'], proxy_dict['port']),
                   'https': 'https://{}:{}'.format(proxy_dict['ip'], proxy_dict['port'])}
        pool.apply_async(check_proxy_func, args=(proxies, proxy_dict, queue_valid))
    pool.close()
    pool.join()


def check_db_proxy_func(proxy, mongo):
    """
    检测数据库中的代理IP，把不可用的代理IP删掉
    """
    proxies = {'http': 'http://{}:{}'.format(proxy[0], proxy[1]),
               'https': 'https://{}:{}'.format(proxy[0], proxy[1])}
    try:
        url = 'http://httpbin.org/ip'
        response = requests.get(url, headers=config.headers, verify=False, proxies=proxies, timeout=10)
        if response.status_code != 200:
            condition = {'ip': proxy[0], 'port': proxy[1]}
            mongo.delete(condition)
    except Exception:
        condition = {'ip': proxy[0], 'port': proxy[1]}
        mongo.delete(condition)


def check_db_proxy(proxy_list):
    """
    检测数据库中的ip
    """
    mongo = MongoHelper()
    count = math.ceil(len(proxy_list) / 10)
    if count == 0:
        return None

    index = 0
    for i in range(1, count+1):
        gevent.joinall(
            [gevent.spawn(check_db_proxy_func, proxy, mongo) for proxy in proxy_list[index: i*10]]
        )
