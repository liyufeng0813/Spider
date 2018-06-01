# -*- coding: utf-8 -*-

import scrapy
from Chinaarea.items import ChinaareaItem


class AirSpiderSpider(scrapy.Spider):
    name = 'air_spider'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']
    base_url = 'https://www.aqistudy.cn/historydata/'

    def parse(self, response):
        url_list = response.xpath('//div[@class="all"]//a/@href').extract()[2:3]
        city_list = response.xpath('//div[@class="all"]//a/text()').extract()[2:3]
        for city, url in zip(city_list, url_list):
            link = '{}{}'.format(self.base_url, url)
            yield scrapy.Request(url=link, callback=self.parse_month, meta={'city': city})

    def parse_month(self, response):
        url_list = response.xpath('//table//tr[position()>1]/td[1]/a/@href').extract()[1:2]
        for url in url_list:
            link = '{}{}'.format(self.base_url, url)
            yield scrapy.Request(url=link, callback=self.parse_day, meta={'city': response.meta['city']})

    def parse_day(self, response):
        node_list = response.xpath('//tbody//tr[position()>1]')
        for node in node_list:
            item = ChinaareaItem()
            item['city'] = response.meta['city']
            item['date'] = node.xpath('./td[1]/text()').extract_first()
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]/span/text()').extract_first()
            item['pm25'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item
