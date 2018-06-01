# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from tencent.items import TencentItem


class TencentHrSpider(RedisSpider):
    name = 'tencent_redis'
    allowed_domains = ['hr.tencent.com']
    # start_urls = ['https://hr.tencent.com/position.php']
    base_url = 'https://hr.tencent.com/'
    redis_key = 'tencent_redis:start_urls'

    def parse(self, response):
        node_list = response.xpath('//tr[@class="even"] | tr[@class="odd"]')

        if not node_list:
            return

        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath('./td[1]/a/text()').extract_first()
            item['position_type'] = node.xpath('./td[2]/text()').extract_first()
            item['people_number'] = node.xpath('./td[3]/text()').extract_first()
            item['work_location'] = node.xpath('./td[4]/text()').extract_first()
            item['publish_time'] = node.xpath('./td[5]/text()').extract_first()
            detail_link = node.xpath('./td[1]/a/@href').extract_first()
            yield scrapy.Request(url=self.base_url + detail_link, callback=self.detail, meta={'item': item})

        next_page = response.xpath('//a[@id="next"]/@href').extract_first()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse)

    def detail(self, response):
        item = response.meta['item']
        node_list = response.xpath('//ul[@class="squareli"]')
        item['job_duties'] = ''.join(node_list[0].xpath('./li/text()').extract())
        item['job_requirement'] = ''.join(node_list[1].xpath('./li/text()').extract())
        yield item
