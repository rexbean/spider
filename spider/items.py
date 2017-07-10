# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    date = scrapy.Field()


class AccountListItem(scrapy.Item):
    accountId = scrapy.Field()
    account = scrapy.Field()
    url = scrapy.Field()
    numPerMon = scrapy.Field()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    account = scrapy.Field()
    accountId = scrapy.Field()
    content = scrapy.Field()

class IpItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    
