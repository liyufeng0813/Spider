import requests
import lxml.html
import re
import csv


douban_url = "https://movie.douban.com/top250?start={}&filter="

def getSource(url):
    """
    获取网页源代码
    :param url:
    :return: String
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36',
    }
    try:
        req = requests.get(url, headers=header, timeout=3)
        req.encoding = 'utf-8'
        return req.content
    except:
        print('爬取失败')

def getEveryItem(source):
    """
    获取每一个电影的相关信息，movie_dict字典用于保存电影的信息。
    :param source:
    :return: [movie1_dict, movie2_dict, movie3_dic, ...]
    """
    selector = lxml.html.document_fromstring(source)
    movieItemList = selector.xpath('//div[@class="info"]')
    form = re.findall(r'<li>(.*?)</li>', source.decode('utf-8'), re.S)[1:]
    movieList = []

    for eachMovie, eachInfo in zip(movieItemList, form):
        movieDict = {}
        title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        otherTitle = eachMovie.xpath('div[@class="hd"]/a/span[@class="other"]/text()')[0]
        link = eachMovie.xpath('div[@class="hd"]/a/@href')[0]
        directorAndActor = eachMovie.xpath('div[@class="bd"]/p[@class=""]/text()')[0]
        star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
        if quote:
            quote = quote[0]
        else:
            quote = ''
        info = re.findall(r'<br>\s*(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)\s*</p>', eachInfo)

        movieDict['title'] = title + otherTitle
        movieDict['url'] = link
        movieDict['directorAndActor'] = directorAndActor.replace(' ','').replace('\n', '')
        movieDict['star'] = star
        movieDict['quote'] = quote
        movieDict['date'] = info[0][0]
        movieDict['site'] = info[0][1]
        movieDict['type'] = info[0][2]
        movieList.append(movieDict)
    return movieList

def writeData(movieList):
    with open('csv/doubanMovie_TOP250.csv', 'w', encoding='utf-8_sig', newline='') as f:
        # excel不能读取utf-8编码,需要指定BOM-utf-8
        writer = csv.DictWriter(f, fieldnames=['title','site','type', 'directorAndActor', 'quote', 'star', 'date', 'url'])
        writer.writeheader()
        for each in movieList:
            writer.writerow(each)


if __name__ == '__main__':
    movieList = []
    for i in range(10):
        pageUrl = douban_url.format(i*25)
        source = getSource(pageUrl)
        movieList += getEveryItem(source)
    movieList = sorted(movieList, key=lambda k:k['star'], reverse=True)
    writeData(movieList)
