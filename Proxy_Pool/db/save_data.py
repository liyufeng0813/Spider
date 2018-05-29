# !/usr/bin/python3
# -*- coding:utf-8 -*-

from db.mongo_helper import MongoHelper


def save_proxy(queue_valid):
    """
    把队列中的ip保存到数据库
    """
    mongo = MongoHelper()
    while not queue_valid.empty():
        try:
            proxy = queue_valid.get()
            if proxy:
                mongo.insert(proxy)
        except Exception as e:
            print('代理保存到数据库时，发生错误: {}'.format(e))
