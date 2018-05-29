# !/usr/bin/python3
# -*- coding:utf-8 -*- 

from lxml import etree


class Parser(object):
    def __init__(self):
        self.parser_dict = {
            'xpath': self.xpath_parser,
        }

    def parser_html(self, html, parser_message):
        """
        主函数：根据配置信息选择不同的解析函数对html进行解析
        """
        return self.parser_dict[parser_message['type']](html, parser_message)

    def xpath_parser(self, html, parser_message):
        """
        xpath解析函数：根据配置文件匹配出Ip地址
        """
        proxy_list = []
        selector = etree.HTML(html)
        items = selector.xpath(parser_message['pattern'])
        for item in items:
            ip = item.xpath(parser_message['position']['ip'])[0].text
            port = item.xpath(parser_message['position']['port'])[0].text
            proxy_dict = {'ip': ip, 'port': port}
            if proxy_dict not in proxy_list:
                proxy_list.append(proxy_dict)
        return proxy_list


if __name__ == '__main__':
    parser_message =     {
        'type': 'xpath',
        'pattern': '//div[@id="list"]/table/tbody/tr',
        'position': {'ip': './td[1]', 'port': './td[2]'},
    }
    url = 'https://www.kuaidaili.com/free/inha/1/'
    import requests
    r = requests.get(url)
    parser = Parser()
    t = parser.parser_html(r.text, parser_message)
    print(t)
