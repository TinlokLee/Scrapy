# -*- coding: utf-8 -*-

from  Sina.items import SinaItem
import scrapy
from scrapy_redis.spider import RedisSpider
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class SinaSpider(RedisSpider):
    name = "sina"
    #allowed_domains = ["sina.com.cn"]
    redis_key = "sinaspider:start_urls"
    #start_urls = [
    #    "http://news.sina.cn/guide"
    #]

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domian', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(SinaSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        ''' 解析所有大类，小类URL和Title '''
        items = []
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitle = response.xpath('//div[@id=\"tab01\"]/div/h3/a/text()').extract()
        subtUrls = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()

        # 爬取所有大类
        for i in range(0, len(parentTitle)):
            # parentFilename = "./Data" + parentTitle[i]
            # if not os.path.exists(parentFilename):
            #     os.mkdirs(parentFilename)
        
        # 爬取所有小类
            for j in range(0, len(subtUrls)):
                item = SinaItem()

                # 保存大类URLS和Title
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

            # 检查小类是否以同类别大类 URL 开头，如果是则返回True
            if_belong = subtUrls[j].startwith(item['parentUrls'])

            # 如果属于大类，将存储目录放在该大类目录下
            if if_belong:
                subFilename = parentFilename + '/' + subTitle[j]
                if not os.path.exists(subFilename):
                    os.mkdir(subFilename)
                
                # 存储小类url,title,filename 字段数据
                item['subUrls'] = subtUrls[j]
                item['subTitle'] = subTitle[j]
                item['subFilename'] = subFilename

                items.append(item)

        # 发送每个小类子链接URL的Request,将得到的response和meta 数据一起交给回调函数detail_parse处理
        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1':item}, callable=self.second_parse)

    # 对于返回小类的url 再次进行递归请求
    def second_parse(self, response):
        ''' 提取数据和所有小类子链接 '''
        meta_1 = response.meta['meta_1']
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(sonUrls)):

            # 检查每个链接是否以大类URL 开头，以HTML 结尾，如果是则返回True
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startwith(meta_1['parentUrls'])
            
            # 如果属于大类，获取字段值放在同一个item 下方便传输
            if if_belong:
                item = SinaItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle'] 
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        # 发送每个小类子链接URL的Request,将得到的response和meta 数据一起交给回调函数detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2':item}, callable=self.detail_parse)

        def detail_parse(self, response): 
            ''' 解析获取文章标题和内容 '''
            item = response.meta['meta_2']
            content = ''
            head = response.xpath('//h1[@id=\"main_title\"].text()')
            content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()

            # 将 P 标签的文本内容合并到一起
            for content_1 in content_list:
                content += content_1

            item['head'] = head[0] if len(head) > 0 else 'NULL'
            item['content'] = content
            yield item
            
