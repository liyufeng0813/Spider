# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class SinaInformationPipeline(object):
    def open_spider(self, spider):
        self.mongo_client = MongoClient(host='127.0.0.1', port=27017)
        self.db = self.mongo_client['sina_information']

    def process_item(self, item, spider):
        data = dict(item)
        if not data['content']:
            return item
        print('=====  ', data, '  =====')
        self.collection = self.db[data['territory']]
        self.collection.insert(data)
        return item

    def close_spider(self, spider):
        self.mongo_client.close()
