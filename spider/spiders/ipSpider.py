#!/usr/bin/python
# -*- coding:utf-8 -*-
import scrapy
import re
import urllib2
from config import proxyList
from scrapy.selector import Selector
from spider.items import IpItem
from utility.utility import Utility
from utility.validateIp import ValidateIp

class IpSpider(scrapy.Spider):

    name = "ip"
    urls = []
    allowed_domains = ["xicidaili.com","66ip.cn"]

    def start_requests(self):
        # for p in proxyList:
            url = proxyList[2]['url'][0]
            print url
            yield scrapy.Request(url,meta={'p':proxyList[2]}, callback=self.parse)

    def parse(self, response):
        ipItem  = IpItem()

        proxy       = response.meta['p']
        rootPath    = proxy['root']
        table       = response.xpath(rootPath).extract()

        for sel in Selector(response=response).xpath(rootPath):
            ipPath      = proxy['ip']
            portPath    = proxy['port']

            ipList      = sel.xpath(ipPath).extract()
            portList    = sel.xpath(portPath).extract()


            ip    =  Utility.listToStr(ipList)
            port  =  Utility.listToStr(portList)
            # using regular expression
            regex   = '\d.{1,3}\d{1,3}'
            if re.match(regex, ip):
                print ip
                v = ValidateIp()
                protocol, anonymous,speed = v.validate(ip,port)
                if protocol is not -1:
                    ipItem['ip']    = ip
                    ipItem['port']  = port
                    print ipItem['ip'],':', ipItem['port']
                    yield ipItem
                else:
                    continue
            else:
                continue






    # def parseIp(self,response):
    #
    #     # print response.body
    #     ipItem  = IpItem()
    #     tablePath      = '//*[@id="ip_list"]/tr'
    #     //*[@id="iptable11"]/tr[1]/td[2]
    #     //*[@id="list"]/table/tr[1]/td[1]
    #     //*[@id="main"]/div/div[1]/table/tbody/tr[2]/td[1]
    #     //*[@id="middle_wrapper"]/div/table/tr[2]/td[1]
    #     /html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr[2]/td[1]
    #     //*[@id="footer"]/div/table/tbody/tr[2]/td[1]
    #     table   = response.xpath(tablePath).extract()
    #     for sel in Selector(response=response).xpath(tablePath):
    #
    #         ip      = sel.xpath('./td[2]/text()').extract()
    #         port    = sel.xpath('./td[3]/text()').extract()
    #
    #         if ip is '':
    #             continue
    #
    #         ipItem['ip']      = Utility.listToStr(ip)
    #         ipItem['port']    = Utility.listToStr(port)
    #
    #         print ipItem['ip'],':',ipItem['port']






        # yield ipItem
