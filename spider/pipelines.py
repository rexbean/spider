# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import urllib
import tempfile
import base64
from spider.utility import Utility

class ArticlePipeline(object):
    def process_item(self, item, spider):
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
