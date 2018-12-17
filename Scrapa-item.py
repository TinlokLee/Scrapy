# -*- coding: utf-8 -*-

import Scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8") 

class SinaItem(scrapy.Item):
    partenTitle = scrapy.Field()
    partenUrls = scrapy.Field()
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()
    subFilename = scrapy.Field()
    sonUrls = scrapy.Field()
    head = scrapy.Field()
    content = scrapy.Field()
