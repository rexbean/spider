# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import urllib
import tempfile
import base64
import settings
import pymongo
from utility.utility import Utility
from spider.items import ArticleItem
from spider.items import IpItem

class ArticlePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item,ArticleItem):
            print'=========================================================='
            p = re.compile(r'(<img(.*?)src=\"(.*?)\")')
            i = 0
            for m in p.finditer(item['content']):
                url = m.group(3)
                filename = './img/article_'+str(i) + '.jpg'
                Utility.getPicFromUrl(url, filename)

                ls_f = Utility.convertPicToBase64(filename)

                item['content'] = item['content'].replace('data-src','src')
                item['content'] = item['content'].replace(m.group(3),'data:image/jpeg;base64,'+ls_f)

                i += 1
                Utility.writeArticleToFile(item)
                return item
class AgentIpStorePipeline(object):
    def __init__(self,host,port,mongo_db,mongo_coll):
        self.host = host
        self.port = port
        self.mongo_db   = mongo_db
        self.mongo_coll = mongo_coll
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host      = crawler.settings.get('MONGO_HOST'),
            port      = crawler.settings.get('MONGO_PORT'),
            mongo_db  = crawler.settings.get('MONGO_DB'),
            mongo_coll= crawler.settings.get('MONGO_COLL')
        )
    def process_item(self, item, spider):
        if isinstance(item,IpItem):
            postItem = dict(item)
            self.coll.insert(postItem)
            return item
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db   = self.client[self.mongo_db]
        self.coll = self.db[self.mongo_coll]
    def close_spider(self, spider):
        self.client.close()



# class ProxyPipeline(object):
#     def process_item(self,item,spider):
#         print'==========================================================='
#         proxy = item['ip']+':'+item['port']
#         print proxy
#         try:
#             proxy_support = urllib2.ProxyHandler({'http':proxy})
#             opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#             urllib2.install_opener(opener)
#             content = urllib2.urlopen('http://192.243.119.61:18080/book',timeout=10).read()
#             print content
#         except:
#             continue
#             print "can't access"
