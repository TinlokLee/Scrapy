import scrapy
import sys

class SinaItem(scrapy.Item):
    # 大类标题和Url
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    # 小类标题和Url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    # 小类目录存储路径
    subFilename = scrapy.Field()

    # 小类下的子链接
    sonUrls = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()

    