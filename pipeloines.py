from scrapy import signals
import sys


class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['sonUrls']
        # 文件名为子链接 url 中间部分，并将 / 替换为 _，保存为 .txt 格式
        filename = sonUrls[7:-6].replace('/','_')
        filename += '.txt'
        
        fp = open(item['subFilename'] + '/' + filename, 'w')
        fp.write(item['content'])
        fp.close()
        return item
