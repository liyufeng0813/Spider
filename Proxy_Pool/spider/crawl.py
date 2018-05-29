# !/usr/bin/python3
# -*- coding:utf-8 -*-

from multiprocessing import Manager

from spider import html_downloader, html_parser, config, check_proxy
from db.save_data import save_proxy
from db.mongo_helper import MongoHelper


class Crawl(object):
    def __init__(self, queue_all, queue_valid):
        self.downloader = html_downloader.Downloader()
        self.parser = html_parser.Parser()
        self.mongo = MongoHelper()

        self.queue_all = queue_all
        self.queue_valid = queue_valid

    def crawl(self, parser_message):
        """
        爬虫主逻辑：
            根据配置信息，对网页进行抓取；
            根据网页解析出其中的ip和port；
            检测ip是否可用，如果可用 则入库。
        """
        for url in parser_message['url_list']:
            html = self.downloader.download_html(url)

            if html:
                proxy_list = self.parser.parser_html(html, parser_message)
                self.save(proxy_list)

            save_proxy(self.queue_valid)

    def save(self, proxy_list):
        """
        对爬到的IP进行去重处理和检测是否可用，如果可用则添加到 proxy_valid 队列中
        """
        for proxy_dict in proxy_list:
            if not self.mongo.select(proxy_dict):
                try:
                    self.queue_all.put(proxy_dict)
                except Exception as e:
                    print('queue_all队列添加时出现错误：{}'.format(e))
        check_proxy.check_proxy(self.queue_all, self.queue_valid)

    def run(self):
        """
        循环检测数据库中的代理是否可用，不可用的删除，如果数据库中的ip个数小于30，启动爬虫程序
        """
        while True:
            proxy_list = self.mongo.select()
            if len(proxy_list) < 30:
                for parser_message in config.parser_message_list:
                    self.crawl(parser_message)
            else:
                print('启动数据库检测函数。')
                check_proxy.check_db_proxy(proxy_list)


def start_crawl(queue_all, queue_valid):
    crawl = Crawl(queue_all, queue_valid)
    crawl.run()


if __name__ == '__main__':
    queue_all = Manager().Queue()
    queue_valid = Manager().Queue()
    crawl = Crawl(queue_all, queue_valid)

    for parser_message in config.parser_message_list:
        crawl.crawl(parser_message)
