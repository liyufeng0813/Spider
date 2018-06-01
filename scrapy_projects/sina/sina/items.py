# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaInformationItem(scrapy.Item):
    # 领域
    territory = scrapy.Field()
    # 分类
    classify = scrapy.Field()
    # 标题
    headline = scrapy.Field()
    # 内容
    content = scrapy.Field()
