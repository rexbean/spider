#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy
import subprocess

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from spider.items import ArticleListItem
from spider.items import ArticleItem
from spider.items import AccountListItem
from spider.utility import Utility


class Test(scrapy.Spider):

    name = "article"
    urls = []
    allowed_domains = ["qq.com"]
    accountListCon = '11002301'
    articleListCon = '11002601'

    start_urls = [
        # search the article with keywords
        "http://weixin.sogou.com/weixin?type=2&query=大数据"
    ]

    def parse(self, response):
        for n in range(9):
            articleListItem = ArticleListItem()
            num = self.articleListCon
            rootPath = '//*[@id="sogou_vr_' + num

            titlePath   = rootPath+'_title_'+str(n)+'"]'
            contentPath = rootPath+'_summary_'+str(n)+'"]'

            title   = response.xpath(titlePath + '//text()').extract()
            url     = response.xpath(titlePath + '/@href').extract()[0]
            content = response.xpath(contentPath + '//text()').extract()

            articleListItem['title']    = Utility.listToStr(title)
            articleListItem['url']      = url
            articleListItem['abstract'] = Utility.listToStr(content)

            print 'title==', articleListItem['title']
            print 'href==',  articleListItem['url']
            print 'content=='
            print articleListItem['abstract']

            yield scrapy.Request(url, callback=self.parseArticle)

    def parseArticle(self, response):
        articleItem = ArticleItem()

        title       = response.xpath('//*[@id="activity-name"]//text()').extract()[0].strip()
        date        = response.xpath('//*[@id="post-date"]//text()').extract()[0]
        author      = response.xpath('//*[@id="img-content"]/div[1]/em[2]').extract()
        account     = response.xpath('//*[@id="post-user"]//text()').extract()[0]
        accountId   = response.xpath('//*[@id="js_profile_qrcode"]/div/p[1]/span//text()').extract()[0]
        content     = response.xpath('//*[@id="js_content"]').extract()

        articleItem['title']    = title.encode('utf-8')
        articleItem['date']     = date.encode('utf-8')
        articleItem['account']  = account.encode('utf-8')
        articleItem['accountId'] = accountId.encode('utf-8')
        articleItem['content'] = Utility.listToStr(content).encode('utf-8')

        if len(author) > 0:
            author = author[0].encode('utf-8')
            articleItem['author'] = author
        else:
            articleItem['author'] = ''

        print articleItem['title']
        Utility.writeArticleToFile(articleItem)
