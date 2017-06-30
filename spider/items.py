# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(serializer='')
    url = scrapy.Field(serializer='')
    account = scrapy.Field(serializer='')
    abtract = scrapy.Field(serializer='')
    date = scrapy.Field(serializer='')
