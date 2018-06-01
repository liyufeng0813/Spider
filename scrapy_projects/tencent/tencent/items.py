# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # 职位名称
    position_name = scrapy.Field()
    # 职位类型
    position_type = scrapy.Field()
    # 需求人数
    people_number = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 工作职责
    job_duties = scrapy.Field()
    # 工作要求
    job_requirement = scrapy.Field()


class TencentItem2(scrapy.Item):
    # 职位名称
    position_name = scrapy.Field()
    # 职位类型
    position_type = scrapy.Field()
    # 需求人数
    people_number = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()


class DetailItem2(scrapy.Item):
    # 工作职责
    job_duties = scrapy.Field()
    # 工作要求
    job_requirement = scrapy.Field()
