#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import scrapy

from spider.items import SpiderItem
from spider.items import ArticleItem


class Test(scrapy.Spider):
    name = "test"
    urls = []
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?type=2&query=大数据"
    ]
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self):
        # init 函数 初始化参数
        keywords = ['大数据']
        for key in keywords:
            self.urls.append("http://weixin.sogou.com/weixin?type=2&query="+key)

        self.logger.info("---- params done ----")

    def parse(self, response):
        for n in range(9):
            articleItem = SpiderItem()

            # title
            titlePath = '//*[@id="sogou_vr_11002601_title_'+str(n)+'"]'
            title = response.xpath(titlePath + '//text()').extract()

            articleItem['title'] = self.appendStr(title)
            print 'title==', articleItem['title']

            # url
            url = response.xpath(titlePath + '/@href').extract()
            articleItem['url'] = url[0]
            yield scrapy.Request(url[0], callback=self.parse_Article)
            print 'href==', articleItem['url']

            # abract
            contentPath = '//*[@id="sogou_vr_11002601_summary_'+str(n)+'"]'
            content = response.xpath(contentPath + '//text()').extract()

            print 'content=='
            articleItem['abtract'] = self.appendStr(content)
            print articleItem['abtract']

    def parse_Article(self, response):
        a = ArticleItem()

        title = response.xpath('//*[@id="activity-name"]//text()').extract()[0].strip()
        a['title'] = title
        print a['title']

        date = response.xpath('//*[@id="post-date"]//text()').extract()[0]
        a['date'] = date.encode('utf-8')

        author = response.xpath('//*[@id="img-content"]/div[1]/em[2]').extract()
        if author is not None:
            a['author'] = author[0].encode('utf-8')

        account = response.xpath('//*[@id="post-user"]//text()').extract()[0]
        a['account'] = account.encode('utf-8')

        accountId = response.xpath('//*[@id="js_profile_qrcode"]/div/p[1]/span//text()').extract()[0]
        a['accountId'] = accountId.encode('utf-8')

        content = response.xpath('//*[@id="js_content"]').extract()
        a['content'] = self.appendStr(content)

        self.writeArticleToFile(a)

    def writeArticleToFile(self, a):
        file = open(a['title']+'.html', 'wb')
        try:
            file.write('<p> title = ' + str(a['title']) + '</p>')
            file.write('<p> date = ' + str(a['date']) + '</p>')
            file.write('<p> author = ' + str(a['author']) + '</p>')
            file.write('<p> account = ' + str(a['account']) + '</p>')
            file.write('<p> accountId =' + str(a['accountId']) + '</p>')
            file.write(a['content'])
        finally:
            file.close()

    def appendStr(self, strList):
        s = ''
        for c in strList:
            s += c
        return s
