import scrapy
from scrapy.selector import Selector
from spider.items import IpItem
from spider.utility import Utility

class IpSpider(scrapy.Spider):

    name = "ip"
    urls = []
    allowed_domains = ["xicidaili.com"]

    header = {
        'Host': 'www.xicidaili.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
    }

    def start_requests(self):
        yield scrapy.Request("http://www.xicidaili.com", headers=self.header, callback = self.parse)

    def parse(self, response):
        Cookie = response.request.headers.getlist('Cookie')
        # print 'Cookie',Cookie
        Cookie = response.headers.getlist('Set-Cookie')
        # print 'Set-Cookie',Cookie

        # for i in range(1,1):
        yield scrapy.Request("http://www.xicidaili.com/nn/2", headers=self.header,cookies={'xicidaili.com':Cookie},callback=self.parseIp)
    def parseIp(self,response):

        # print response.body
        ipItem  = IpItem()
        tablePath      = '//*[@id="ip_list"]/tr'
        table   = response.xpath(tablePath).extract()
        for sel in Selector(response=response).xpath(tablePath):

            ip      = sel.xpath('./td[2]/text()').extract()
            port    = sel.xpath('./td[3]/text()').extract()

            ipItem['ip']      = Utility.listToStr(ip)
            ipItem['port']    = Utility.listToStr(port)

            print ipItem['ip'],':',ipItem['port']





        # yield ipItem
