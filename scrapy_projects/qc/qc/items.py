# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QcItem(scrapy.Item):
    # 职位名称
    job = scrapy.Field()
    # 公司名称
    company = scrapy.Field()
    # 工作地点
    workplace = scrapy.Field()
    # 薪资范围
    salary = scrapy.Field()
    # 发布时间
    pubdate = scrapy.Field()
    # 学历要求
    education = scrapy.Field()
    # 经验要求
    experience = scrapy.Field()
    # 人数
    number = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 详情页内容
    job_information = scrapy.Field()
    # 联系方式
    contact = scrapy.Field()
    # 数据源
    source = scrapy.Field()
    # 抓取时间
    utc_time = scrapy.Field()
