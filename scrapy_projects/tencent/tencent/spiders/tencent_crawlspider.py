# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tencent.items import TencentItem2, DetailItem2


class Tencent3Spider(CrawlSpider):
    name = 'tencent_crawlspider'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_tencent', follow=True),
        Rule(LinkExtractor(allow=r'position_detail'), callback='parse_detail', follow=False),
    )

    def parse_tencent(self, response):
        node_list = response.xpath('//tr[@class="even"] | tr[@class="odd"]')

        if not node_list:
            return

        for node in node_list:
            item = TencentItem2()
            item['position_name'] = node.xpath('./td[1]/a/text()').extract_first()
            item['position_type'] = node.xpath('./td[2]/text()').extract_first()
            item['people_number'] = node.xpath('./td[3]/text()').extract_first()
            item['work_location'] = node.xpath('./td[4]/text()').extract_first()
            item['publish_time'] = node.xpath('./td[5]/text()').extract_first()
            yield item

    def parse_detail(self, response):
        item = DetailItem2()
        node_list = response.xpath('//ul[@class="squareli"]')
        item['job_duties'] = ''.join(node_list[0].xpath('./li/text()').extract())
        item['job_requirement'] = ''.join(node_list[1].xpath('./li/text()').extract())
        yield item
