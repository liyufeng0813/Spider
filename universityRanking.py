import requests
from bs4 import BeautifulSoup
import bs4


def getHtml(url):
    """
    获取网页HTML
    :param url:
    :return: HTML
    """
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def universityList(uList, html):
    """
    获取大学排名信息
    :param uList: []
    :param html:
    :return: universityList
    """
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            uList.append([tds[0].string, tds[1].string, tds[2].string])

def printUniversityList(uList, num):
    """
    格式化输出排名
    :param uList:
    :param num:
    :return:
    """
    print('{0:^10}\t{1:{3}^10}\t{2:^10}'.format('排名', '学校名称', '评分', chr(12288)))    # 用中文间隔填充
    for i in range(num):
        u = uList[i]
        print('{0:^10}\t{1:{3}^10}\t{2:^10}'.format(u[0], u[1], u[2], chr(12288)))


def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2016.html'
    html = getHtml(url)
    universityList(uinfo, html)
    printUniversityList(uinfo, 20)


if __name__ == '__main__':
    main()