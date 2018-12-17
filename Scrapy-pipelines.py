# -*- coding: utf-8 -*-

from scrapy import singals
import sys

class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['sonUrls']
        filename = sonUrls[7:-6].replace('/','_')
        filename += ".txt"
        fp = open(item['subFilename'] + '/' + filename, 'w')
        fp.write(item['content'])
        fp.close()
        return item
        
