import urllib.request, urllib.error
import http.cookiejar
import lxml.html


def getHtml(url):
    """
    获取网页源代码
    :param url:
    :return: Html
    """
    cookieJar = http.cookiejar.CookieJar()  #创建CookieJar对象
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))   #使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
    urllib.request.install_opener(opener)   #将opener安装到request中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    try:
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode()
        return html
    except:
        return ''

def getIpAndPortList(html):
    """
    获取网页源代码中的IP和PORT，并且返回装着所有IP和PORT的列表。
    :param html:
    :return: ip和端口的列表
    """
    selector = lxml.html.fromstring(html)
    IP = selector.xpath('//td[@data-title="IP"]/text()')
    PORT = selector.xpath('//td[@data-title="PORT"]/text()')
    ipAndPortList = []
    for eachIp,eachPort in zip(IP, PORT):
        eachList = str(eachIp) + ':' + str(eachPort)
        ipAndPortList.append(eachList)
    return ipAndPortList

def verifyIp(ipAndPortList):
    """
    验证IP是否可以代理,返回装着可使用的ip列表。
    :param ipAndPortList:
    :return: 可代理使用的ip列表
    """
    url = 'http://httpbin.org/ip'
    ipList = []
    for ipAndPort in ipAndPortList:
        try:
            proxy = {'http': ipAndPort, 'https': ipAndPort}
            proxies = urllib.request.ProxyHandler(proxy)    # 创建代理处理器
            opener = urllib.request.build_opener(proxies, urllib.request.HTTPHandler)   # 创建特定的opener对象
            urllib.request.install_opener(opener)
            print(ipAndPort)
            urllib.request.urlopen(url=url)   # 通过访问url，检测ip是否可用
        except (urllib.error.URLError, ConnectionResetError):
            index = ipAndPortList.index(ipAndPort)
            del ipAndPortList[index]
        else:
            ipList.append(ipAndPort)
    return ipList


if __name__ == '__main__':
    ipUrl = "https://www.kuaidaili.com/free/inha/{}/"
    reusabilityIp = []
    for num in range(1, 2117):
        try:
            ipUrl = ipUrl.format(num)
            html = getHtml(ipUrl)
            ipAndPortList = getIpAndPortList(html)
            ipList = verifyIp(ipAndPortList)
            if len(ipList) == 0:
                continue
            reusabilityIp.append(ipList)
        except:
            continue
    print(reusabilityIp)
