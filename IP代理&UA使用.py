'''
    Scrapy 代理IP、User-Agent的切换通过DOWNLOADER_MIDDLEWARES控制
    在 settings.py 同级目录下创建 middlewares.py 使用

'''
import random
import base64
from settings import PROXIES


# 随机使用预定义列表中的 User-Agent
class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod 
    def from_crawler(cls, crawler):
        # 获取settings 的USER_AGENT 列表并返回
        return cls(crawler.settings.getlist('USER_AGENTS'))
    
    def process_request(self, request, spider):
        # 随机设置 Request 报头中 Header的 User-Agent
        request.headers.setdefault('User-Agent', random.choice(self.agents))


# 随机使用预定义列表的 Proxy 
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['User-pass'] is not None:
            request.meta['proxy'] = 'http"//%s' % proxy['ip_port']
            # 对代理数据进行 Base64 编码
            encoded_user_pass = base64.encodestring(proxy['User-pass'])
            # 添加到 HTTP 代理格式中
            request.headers['Proxy-Authorization'] = 'Basic' + encoded_user_pass
        else:
            pring('******代理失效******' + proxy['ip_port'])
            request.meta['proxy'] = 'http://%s' % proxy['ip_port']



# settings.py
# 添加User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0
; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729
; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64;
Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.
50727; Media Center PC 6.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre)
Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/
20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.
4.5"
]

PROXIES = [
    {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
    {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    {'ip_port': '120.198.243.22:80', 'password': ''}
]

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 1.5

DOWNLOADER_MIDDLEWARES = {
#'mySpider.middlewares.MyCustomDownloaderMiddleware': 543,
'mySpider.middlewares.RandomUserAgent': 1,
'mySpider.middlewares.ProxyMiddleware': 100
}