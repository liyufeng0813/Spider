# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import pymongo
import pymysql


def check_saving_mode(mode):
    def wrapper(func):
        def inner(*args):
            if args[1].saving_mode == mode:
                return func(*args)
        return inner
    return wrapper


class QcJsonPipeline(object):

    @check_saving_mode('json')
    def open_spider(self, spider):
        self.file = open('qc/data/qc.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.saving_mode == 'json':
            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(content)
        return item

    @check_saving_mode('json')
    def close_spider(self, spider):
        self.file.close()


class QcMongoPipeline(object):

    @check_saving_mode('mongodb')
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.collection = self.client['qc']['qc']

    def process_item(self, item, spider):
        if spider.saving_mode == 'mongodb':
            self.collection.insert(dict(item))
        return item

    @check_saving_mode('mongodb')
    def close_spider(self, spider):
        self.client.close()


class QcMysqlPipeline(object):

    @check_saving_mode('mysql')
    def open_spider(self, spider):
        self.con = pymysql.connect(host="localhost", port=3306, database="qc", charset="utf8",
                                   user="root", password="root")
        self.cursor = self.con.cursor()
        create_database = """
                        create table if not exists `qc`(
                        id int primary key auto_increment,
                        job varchar(100) default '',
                        company varchar(100) default '',
                        workplace varchar(30) default '',
                        salary varchar(30) default '',
                        pubdate varchar(30) default '',
                        education varchar(30) default '',
                        experience varchar(30) default '',
                        `number` varchar(30) default '',
                        tag varchar(100) default '',
                        jobInformation varchar(2000) default '',
                        contact varchar(200) default '',
                        source varchar(20) default '',
                        utcTime varchar(30) default '') ENGINE=INNODB  DEFAULT CHARSET=utf8;
                        """
        self.cursor.execute(create_database)
        self.con.commit()

    def process_item(self, item, spider):
        if spider.saving_mode == 'mysql':
            sql = """insert into qc(job, company, workplace, salary, pubdate, education, 
                        experience, `number`, tag, jobInformation, contact, source, utcTime) values(%s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            values = (item['job'], item['company'], item['workplace'], item['salary'], item['pubdate'],
                          item['education'], item['experience'], item['number'], item['tag'], item['job_information'],
                          item['contact'], item['source'], item['utc_time'])
            self.cursor.execute(sql, values)
            self.con.commit()
        return item

    @check_saving_mode('mysql')
    def close_spider(self, spider):
        self.con.close()
        self.cursor.close()
