# !/usr/bin/python3
# -*- coding:utf-8 -*- 

import pymongo
from pymongo.errors import WriteError


class MongoHelper(object):
    def __init__(self):
        connect = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = connect.proxy
        self.collection = db.proxies

    def insert(self, proxy):
        try:
            proxy = dict(ip=proxy['ip'], port=proxy['port'], speed=proxy['speed'])
        except KeyError:
            return ''
        self.collection.insert(proxy)

    def delete(self, condition):
        if condition:
            self.collection.remove(condition)

    def update(self, condition, value):
        if condition and value:
            try:
                self.collection.update(condition, {'$set': value})
            except (WriteError, TypeError):
                print('条件为: {} 的数据修改出现错误。'.format(condition))

    def select(self, condition=None, count=0):
        condition = condition if condition is not None else {}
        result = []
        try:
            items = self.collection.find(condition, limit=count)
        except TypeError:
            return result

        for item in items:
            result.append([item['ip'], item['port']])
        return result


if __name__ == '__main__':
    mongo = MongoHelper()
    a = mongo.select()
    print(a)
