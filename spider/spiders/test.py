#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from spider.items import SpiderItem


class Test(scrapy.Spider):
    name = "test"
    urls = []
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?type=2&query=大数据"
    ]

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
            articleItem['url'] = url
            scrapy.request(url, callback=self.parseArticle)
            print 'href==', articleItem['url']

            # abract
            contentPath = '//*[@id="sogou_vr_11002601_summary_'+str(n)+'"]'
            content = response.xpath(contentPath + '//text()').extract()

            print 'content=='
            articleItem['abtract'] = self.appendStr(content)
            print articleItem['abtract']

    def parseArticle(self, response):


    def appendStr(self, strList):
        s = ''
        for c in strList:
            s += c
        return s
