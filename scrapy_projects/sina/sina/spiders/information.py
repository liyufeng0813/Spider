# -*- coding: utf-8 -*-
import scrapy

from sina.items import SinaInformationItem


class InformationSpider(scrapy.Spider):
    name = 'information'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        """
        解析每个板块，获取板块下面的所有分类
        """
        territory_node_list = response.xpath('//div[@id="tab01"]/div[@class="clearfix"]')

        for territory_node in territory_node_list:
            territory_title = territory_node.xpath('.//h3[@class="tit02"]//text()').extract_first()
            territory_url = territory_node.xpath('.//h3[@class="tit02"]/a/@href').extract_first()
            classify_url_list = territory_node.xpath('.//ul[@class="list01"]/li/a/@href').extract()
            classify_title_list = territory_node.xpath('.//ul[@class="list01"]/li/a/text()').extract()

            for index in range(0, len(classify_url_list)):
                classify_url = classify_url_list[index]
                classify_title = classify_title_list[index]
                yield scrapy.Request(url=classify_url,
                                     callback=self.parse_classify,
                                     meta={'territory_title': territory_title,
                                           'classify_title': classify_title,
                                           'territory_url': territory_url})

    def parse_classify(self, response):
        """
        解析每个分类，获取这个分类下有用的a标签，再继续解析a标签对应的文章
        """
        territory_url = response.meta['territory_url']
        if territory_url:
            article_link_list = response.xpath('//a[starts-with(@href, "{}") and contains(@href, ".shtml")]/@href'.format(territory_url)).extract()
        else:
            article_link_list = response.xpath('//a[contains(@href, ".shtml")]/@href').extract()

        for article_link in article_link_list:
            item = SinaInformationItem()
            item['territory'] = response.meta['territory_title']
            item['classify'] = response.meta['classify_title']
            yield scrapy.Request(url=article_link, callback=self.parse_article, meta={'item': item})

    def parse_article(self, response):
        """
        解析每个文章
        """
        item = response.meta['item']
        headline = response.xpath('//h1[@class="main-title" or @id="artibodyTitle" or @id="main_title"]/text()').extract_first()
        content = "".join(response.xpath('//div[@id="article" or @id="artibody"]//p[position() > 1 and position() < last()]/text()').extract())
        item['headline'] = headline
        item['content'] = content
        yield item
