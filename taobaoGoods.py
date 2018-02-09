# !/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
import csv

def getHtml(url):
    """
    get the webpage source code.
    :param url:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ''

def parsePage(html, infoList):
    """
    parse html,return commodity infomation list.
    :param html:
    :return: infoList
    """
    try:
        price = re.findall(r'"view_price":"(.*?)"', html)
        num = len(price)
        title = re.findall(r'"raw_title":"(.*?)"', html)
        sales = re.findall(r'"view_sales":"(\d+)人付款"', html)
        taobaoID = re.findall(r'"nick":"(.*?)"', html)[:num]
        location = re.findall(r'"item_loc":"(.*?)"', html)
        for i in range(num):
            infoList.append([title[i], price[i], sales[i], taobaoID[i], location[i]])
        return infoList
    except:
        return ''

def writeCommodity(infoList):
    """
    write the commodity list to the taobaoCommodity.csv file,
    :param infoList:
    :return:
    """
    with open('csv/书包.csv', 'w', encoding='utf-8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['名称', '价格', '付款人数', '淘宝ID', '店铺地址'])
        writer.writerows(infoList)

def main():
    commodity = '书包'
    depth = 101
    infoList = []
    for i in range(depth):
        try:
            i *= 44
            url = 'https://s.taobao.com/search?q={}&s={}'.format(commodity, i)
            html = getHtml(url)
            infoList = parsePage(html, infoList)
        except:
            continue
    infoList = sorted(infoList, key=lambda x:int(x[2]), reverse=True)   # 商品按销量降序排列
    writeCommodity(infoList)


if __name__ == '__main__':
    main()
