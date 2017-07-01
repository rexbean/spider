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
from articleSpider import ArticleSpider


class AccountSpider(scrapy.Spider):

    name = "account"
    urls = []
    allowed_domains = ["qq.com"]
    accountListCon = '11002301'
    articleListCon = '11002601'

    start_urls = [
        # search the account with keyword
         "http://weixin.sogou.com/weixin?type=1&query=大数据"

    ]

    def parse(self, response):
        for n in range(1):
            accountListItem = AccountListItem()
            num             = self.accountListCon

            rootPath        = '//*[@id="sogou_vr_'+num+'_box_'+str(n)+'"]'
            accountIdPath   = './div/div[2]/p[2]/label//text()'

            txtBox          = response.xpath(rootPath)
            accountId       = txtBox.xpath(accountIdPath).extract()

            accountName = txtBox.xpath('./div/div[2]/p[1]/a//text()').extract()
            url         = txtBox.xpath('./div/div[2]/p[1]/a/@href').extract()[0]


            accountListItem['account']      = Utility.listToStr(accountName)
            accountListItem['url']          = url
            accountListItem['accountId']    = accountId[0].encode('utf-8')

            print accountListItem['account']
            print accountListItem['url']
            print accountListItem['accountId']

            url.replace('http', 'https')

            cmd = "phantomjs ./getBody.js '%s'" % url
            stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE).communicate()
            r = HtmlResponse(url=url, body=stdout)

            articleUrls = self.parseAccount(r)
            for url in articleUrls:
                yield scrapy.Request(url, callback=ArticleSpider().parseArticle)

    def parseAccount(self, response):
            urls = []
            articleListItem = ArticleListItem()
            account = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/strong//text()').extract()[0].strip()
            print '----------------------'+account+'-------------------------'
            for articlePath in Selector(response=response).xpath('//*[@class="weui_media_box appmsg"]/div'):
                # title
                title = articlePath.xpath('./h4//text()').extract()[0].strip()
                articleListItem['title'] = title
                print articleListItem['title']
                # url
                url = articlePath.xpath('./h4//@hrefs').extract()[0]
                url = "https://mp.weixin.qq.com"+url
                articleListItem['url'] = url

                print articleListItem['url']
                # date
                date = articlePath.xpath('.//*[@class="weui_media_extra_info"]//text()').extract()[0]
                articleListItem['date'] = date
                print articleListItem['date']
                # abstract
                abstract = articlePath.xpath('.//*[@class="weui_media_desc"]//text()').extract()
                articleListItem['abstract'] = Utility.listToStr(abstract)
                print articleListItem['abstract']

                urls.append(url)
            return urls
