#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy

from spider.items import ArticleListItem
from spider.items import ArticleItem
from spider.items import AccountListItem
from scrapy.selector import Selector


class Test(scrapy.Spider):

    name = "test"
    allowed_domains = ["qq.com"]
    accountListCon = '11002301'
    articleListCon = '11002601'

    start_urls = [
        # search the article with keywords
        # "http://weixin.sogou.com/weixin?type=2&query=大数据"
        # search the account with keyword
        "http://weixin.sogou.com/weixin?type=1&query=大数据"

    ]

    def parse(self, response):
        kind = response.xpath('/html/head/title//text()').extract()[0]
        if unicode('文章', encoding='utf-8') in kind:
            print 'article'
            yield self.parseArticleList(response)
        else:
            print 'account'
            yield self.parseAccountList(response)

    def parseAccountList(self, response):
        for n in range(9):
            accountListItem = AccountListItem()
            # path
            accountPath = '//*[@id="sogou_vr_'+self.accountListCon+'_box_'+str(n)+'"]'
            txtBox = response.xpath(accountPath)
            # accountName
            accountName = txtBox.xpath('./div/div[2]/p[1]/a//text()').extract()
            accountListItem['account'] = self.listToStr(accountName)
            print accountListItem['account']
            # url
            url = txtBox.xpath('./div/div[2]/p[1]/a/@href').extract()[0]
            accountListItem['url'] = url
            yield scrapy.Request(url, callback=self.parseAccount)
            print accountListItem['url']
            # number of articles pubulished per month
            numPerMonPath = './div/div[2]/p[2]/label//text()'
            a = txtBox.xpath(numPerMonPath).extract()
            accountListItem['accountId'] = a[0].encode('utf-8')
            print accountListItem['accountId']

    def parseAccount(self, response):
            articleListItem = ArticleListItem()
            account = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/strong//text()').extract()[0].strip()
            print '----------------------'+account+'-------------------------'
            for articlePath in Selector(response=response).xpath('//*[@class="weui_media_box appmsg"]/div'):
                # title
                title = articlePath.xpath('./h4//text()').extract[0].strip()
                articleListItem['title'] = title
                print articleListItem['title']
                # url
                url = articlePath.xpath('./h4//@href').extract[0]
                articleListItem['url'] = url
                print articleListItem['url']
                # date
                date = articlePath.xpath('.//*[@class="weui_media_extra_info"]//text()').extract()[0]
                articleListItem['date'] = date
                print articleListItem['date']
                # abstract
                abstract = articlePath.xpath('.//*[@class="weui_media_desc"]//text()').extract()
                articleListItem['abstract'] = self.listToStr(abstract)
                print articleListItem['abstract']

    def parseArticleList(self, response):
        for n in range(9):
            articleListItem = ArticleListItem()

            # title
            titlePath = '//*[@id="sogou_vr_'+self.articleListCon+'_title_'+str(n)+'"]'
            title = response.xpath(titlePath + '//text()').extract()

            articleListItem['title'] = self.listToStr(title)
            print 'title==', articleListItem['title']

            # url
            url = response.xpath(titlePath + '/@href').extract()[0]
            articleListItem['url'] = url
            yield scrapy.Request(url, callback=self.parseArticle)
            print 'href==', articleListItem['url']

            # abstract
            contentPath = '//*[@id="sogou_vr_'+self.articleListCon+'_summary_'+str(n)+'"]'
            content = response.xpath(contentPath + '//text()').extract()

            print 'content=='
            articleListItem['abstract'] = self.listToStr(content)
            print articleListItem['abstract']

    def parseArticle(self, response):
        articleItem = ArticleItem()

        title = response.xpath('//*[@id="activity-name"]//text()').extract()[0].strip()
        articleItem['title'] = title
        print articleItem['title']

        date = response.xpath('//*[@id="post-date"]//text()').extract()[0]
        articleItem['date'] = date.encode('utf-8')

        author = response.xpath('//*[@id="img-content"]/div[1]/em[2]').extract()
        if author is not None:
            articleItem['author'] = author[0].encode('utf-8')

        account = response.xpath('//*[@id="post-user"]//text()').extract()[0]
        articleItem['account'] = account.encode('utf-8')

        accountId = response.xpath('//*[@id="js_profile_qrcode"]/div/p[1]/span//text()').extract()[0]
        articleItem['accountId'] = accountId.encode('utf-8')

        content = response.xpath('//*[@id="js_content"]').extract()
        articleItem['content'] = self.listToStr(content)

        self.writeArticleToFile(articleItem)

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

    def listToStr(self, strList):
        s = ''
        for c in strList:
            s += c
        return s
