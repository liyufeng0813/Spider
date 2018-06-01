# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import pymongo

from tencent.items import TencentItem, TencentItem2, DetailItem2
from tencent.settings import BASE_DIR


class TencentPipeline(object):

    def open_spider(self, spider):

        if spider.name == 'tencent_redis':
            file_path = os.path.join(BASE_DIR, 'data/tencent.json')
            self.file = open(file_path, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, TencentItem):
            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(content)
        return item

    def close_spider(self, spider):
        if spider.name == 'tencent_redis':
            self.file.close()


class TencentPipeline2(object):

    def open_spider(self, spider):
        if spider.name == 'tencent_crawlspider':
            self.file1 = open('tencent4.json', 'w', encoding='utf-8')
            self.file2 = open('tencentdetail4.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        if isinstance(item, TencentItem2):
            self.file1.write(content)
        elif isinstance(item, DetailItem2):
            self.file2.write(content)
        return item

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()


# class TencentPipeline2(object):
#
#     def __init__(self):
#         client = pymongo.MongoClient()
#         db = client.tencent
#         self.col1 = db.tencent_hr
#         self.col2 = db.tencent_detail
#
#     def process_item(self, item, spider):
#         if isinstance(item, TencentItem2):
#             self.col1.insert(dict(item))
#         else:
#             self.col2.insert(dict(item))
#         return item
