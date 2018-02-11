# Spider

## 请求库

#### 1- urllib库

- urllib.request	请求模块
- urllib.error             异常处理模块
- urllib.parse           url解析模块
- urllib.robotparse    robots.txt解析模块

```python
import urllib.request

response = urllib.request.urlopen('http://www.baidu.com')
print(response.read().decode('utf-8'))
# read() 返回的是 bytes类型。

import urllib.parse
data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf-8')
# 传入的data需要为 bytes类型数据
r = urllib.request.urlopen('http://httpbin.org/post', data=data)
# url编码
parse.quote
>>> urllib.parse.quote('{}')
'%7B%7D'
parse.unquote
>>> urllib.parse.unquote('%7B%7D')
'{}'

##  响应	##
response.read().decode('utf-8')	#read读取的是bytes类型，转成utf-8编码。
response.status		# statuscode
response.getheaders()

##  request  ##
url = "http://httpbin.org/post"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
dict = {
    'name': 'mike'
}
data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
r = urllib.request.urlopen(req)

##  设置代理 ##
url = 'http://httpbin.org/ip'
proxy = {'http':'39.134.108.89:8080','https':'39.134.108.89:8080'}
proxies = urllib.request.ProxyHandler(proxy) # 创建代理处理器
opener = urllib.request.build_opener(proxies,urllib.request.HTTPHandler) # 创建特定的opener对象
urllib.request.install_opener(opener) # 安装全局的opener 把urlopen也变成特定的opener
data = urllib.request.urlopen(url)
print(data.read().decode())

##  设置cookies  ##
import urllib.request
import http.cookiejar

url = 'https://www.jianshu.com'
# 创建CookieJar对象
cookie_jar = http.cookiejar.CookieJar()
#使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener=urllib.request.build_opener(handler)
# 安装opener
urllib.request.install_opener(opener)
data = urllib.request.urlopen(url)
print(cookie_jar)

```

###urllib.error

urllib.error中常用的有两个方法，URLError和HTTPError,HTTPError是URLError的一个子类。

**URLError**产生原因一般是:网络无法连接、服务器不存在等。例如访问一个不存在的url。



###urllib.parse

urllib.parse.urljoin 拼接url
urllib.parse.urlencode 字典转字符串
urllib.parse.quote url编码
urllib.parse.unquote url解码
Url的编码格式采用的是ASCII码，而不是Unicode，





##解析库

####1- lxml库

​	语法：XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。XPath 是 W3C XSLT 标准的主要元素，并且 XQuery 和 XPointer 都构建于 XPath 表达之上。

```python
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chapter11_example_2</title>
</head>
<body>
<ul class="item">
    <li class="name">无人机</li>
    <li class="price">1亿</li>
</ul>
<ul class="item">
    <li class="name">火箭炮</li>
</ul>
</body>
</html>
"""
import lxml.html
selector = lxml.html.fromstring(html)
# 查找无人机
1，属性前面要加 @，
>>> selector.xpath('//ul[@class="item"]/li[@class="name"]/text()')
['无人机', '火箭炮']

# li标签的class属性值
>>> selector.xpath('//li/@class')
['name', 'price', 'name']

# html中有两个ul标签，可以先抓大再抓小
>>> ul = selector.xpath('//ul[@class="item"]')	 # 先抓整体
>>> ul[0].xpath('li[@class="price"]/text()')
['1亿']

"""
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>"""
# 获取最后一个 li 标签 a 标签的 href 属性
result = html.xpath('//li[last()]/a/@href')

# 获取class为bold的标签名
result = html.xpath('//*[@class="bold"]')

#获取 <li> 标签下的所有 <span> 标签
result = html.xpath('//li/span')    # 错误，因为 / 是用来获取子元素的，而 <span> 并不是 <li> 的子元素，所以，要用双斜杠
result = html.xpath('//li//span')
```

#### 2- pyquery库

