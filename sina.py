# -*- coding:utf-8 -*-

from Sina.items import SinaItem
import scrapy
import os
import sys


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/guide/"]

    def pasrse(self, response):
        items = []
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitle = response.xpath("//div[@id=\"tab01\"]/div/h3/a/text()").extract()
        subUrls = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()

        # 获取所有大类
        for i in range(0, len(parentTitle)):
            parentFilename = "./Data/" +　parentTitle[i]
            if not os.path.exists(parentFilename):
                os.makedirs(parentFilename)
            
            # 获取所有小类
            for j in range(0, len(subUrls)):
                item = SinaItem()

                # 保存大类的title和urls
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

                # 检查小类的 url 是否以同类别大类 url 开头，如果是返回True
                if_belong = subUrls[j].startswith(item['parentUrls'])

                # 如果属于大类，将存储目录放在该大类目录下
                if if_belong:
                    sunFilename = parentFilename + '/' + subTitle[j]
                    if not os.path.exists(sunFilename):
                        os.makedirs(sunFilename)
                    
                    # 存储小类 url、title 和 filename 字段数据
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] =subTitle[j]
                    item['subFilename'] = subFilename
                    items.append(item)
        # 发送每个小类 url 的 Request 请求，得到 Response 连同包含 meta 数据
        # 一同交给回调函数 second_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['subUrls'],meta={'meta_1':item},callback=self.second_parse)

    # 对于返回的小类Url,再进行递归请求
    def second_parse(self, response):
        meta_1 = response.meta['meta_1']

        # 取出小类里所有子链接
        sonUrls = response.xpath('.//a/@href').extract()
        items = []
        for i in range(0, len(sonUrls)):
            # 检查每个链接是否以⼤类 url 开头、以.shtml 结尾，如果是返回True
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            # 若果属于该大类，获取字段值放在同一个item传输
            if if_belong:
                item = SinaItem()
                item['parentTitle'] =meta_1['parentTitle']
                item['parentUrls'] =meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        #发送每个小类下子链接 url的 Request，得到 Response 后
        # 连同包含 meta 数据一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2':item}, callback = self.detail_parse)
    
    # 解析数据，获取文章标题内容
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id=\"main_title\"]/text()')
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()

        # 将 p 标签的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['head'] = head
        item['content'] = content
        yield item













