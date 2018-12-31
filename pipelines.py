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


'''
    数据存储MongoDB
'''
from scrapy.conf import settings
import pymongo

class SinaPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)

        mdb = client[dbname]
        self.post = mdb[settings['MONGODB_DBNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item



