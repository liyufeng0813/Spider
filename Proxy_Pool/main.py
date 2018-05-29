# !/usr/bin/python3
# -*- coding:utf-8 -*-

from multiprocessing import Process, Manager

from spider.crawl import start_crawl
from web.web_server import start_server


def main():
    queue_all = Manager().Queue()
    queue_valid = Manager().Queue()

    spider_process = Process(target=start_crawl, args=(queue_all, queue_valid))
    web_server = Process(target=start_server)
    spider_process.start()
    web_server.start()

    spider_process.join()
    web_server.join()


if __name__ == '__main__':
    main()
