# -*- coding: utf-8 -*-

import time

import scrapy
from qc.items import QcItem


class QcxySpider(scrapy.Spider):
    name = 'qcwy'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']
    saving_mode = 'mysql'	# 存储数据模式支持：json文件、mongodb、mysql

    def parse(self, response):
        node_list = response.xpath('//div[@class="el"]')
        next_url = response.xpath('//li[@class="bk"]/a[contains(text(), "下一页")]/@href').extract_first()
        for node in node_list:
            detail_href = node.xpath('./p/span/a[starts-with(@href, "https://jobs.51job.com/")]/@href').extract_first()
            if not detail_href:
                continue
            item = QcItem()
            item['job'] = node.xpath('./p/span/a/@title').extract_first().strip()
            yield scrapy.Request(detail_href, callback=self.detail_parse, meta={'item': item})
        yield scrapy.Request(next_url, callback=self.parse)

    def detail_parse(self, response):
        item = response.meta['item']
        item['company'] = response.xpath('//p[@class="cname"]/a/text()').extract_first()
        item['workplace'] = response.xpath('//span[@class="lname"]/text()').extract_first()
        item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract_first()
        item['pubdate'] = response.xpath('//em[@class="i4"]/../text()').extract_first()
        item['education'] = response.xpath('//em[@class="i2"]/../text()').extract_first()
        item['experience'] = response.xpath('//em[@class="i1"]/../text()').extract_first()
        item['number'] = response.xpath('//em[@class="i3"]/../text()').extract_first()

        tag_node = response.xpath('//p[@class="t2"]')
        try:
            item['tag'] = tag_node.xpath('string(.)').extract_first().replace('\r\n', ',').replace('\t', '').strip(',')
        except:
            item['tag'] = ''

        info_node = response.xpath('//div[@class="bmsg job_msg inbox"]/p')
        try:
            item['job_information'] = info_node.xpath('string(.)').extract_first()
        except:
            item['job_information'] = ''

        item['contact'] = ''.join(response.xpath('//div[@class="bmsg inbox"]//p[@class="fp"]/text()').extract()).strip()
        item['source'] = '前程无忧'
        item['utc_time'] = time.strftime('%Y年%m月%d日%H时%m分%S秒', time.localtime(time.time()))
        yield item
