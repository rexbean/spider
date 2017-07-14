# coding:utf-8
import sys
import json
import os
import requests
import random
import time
import config



class ValidateIp(object):

    def validate(self,ip,port):
        proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
        return self.getProtocol(proxies)
    def getProtocol(self,proxies):
        anonymous = -1
        speed = -1

        # for http
        url = config.TEST_HTTP_HEADER
        http,anonymous,speed = self.getType(proxies, url)

        #for https
        url = config.TEST_HTTPS_HEADER
        https,anonymous,speed = self.getType(proxies,url)

        if http and https:
            protocol = 2
        elif https:
            protocol = 1
        elif http:
            protocol = 0
        else:
            protocol = -1
        print 'protocol',protocol,'anonymous',anonymous,'speed',speed
        return protocol, anonymous, speed

    def getType(self, proxies, url):
        types = -1
        speed = -1
        try:
            start = time.time()
            r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
            if r.ok:
                speed = round(time.time() - start, 2)
                content = json.loads(r.text)
                headers = content['headers']
                ip = content['origin']
                proxy_connection = headers.get('Connection', None)
                # print 'proxy_connection',proxy_connection
                if ',' in ip:
                    anonymous = 2
                elif proxy_connection:
                    anonymous = 1
                else:
                    anonymous = 0
                return True, types, speed
            else:
                return False, types, speed
        except Exception as e:
            print 'error'
            return False, types, speed




    # @staticmethod
    # def validateByWebSite(self,url,ip,port):
if __name__ == '__main__':
    ip = '121.69.47.126'
    port = 8080
    # proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
    # v = ValidateIp()
    # print v.get_header()
    # print proxies
    # url = v.TEST_HTTP_HEADER
    # r = requests.get(url=url, headers=v.get_header(), timeout=10, proxies=proxies)
    # start = time.time()
    # if r.ok:
    #     speed = round(time.time() - start, 2)
    #     content = json.loads(r.text)
    #     headers = content['headers']
    #     ip = content['origin']
    #     proxy_connection = headers.get('Proxy-Connection', None)
    #     print 'header=',headers
    # getMyIP()
    # str="{ip:'61.150.43.121',address:'陕西省西安市 西安电子科技大学'}"
    # j = json.dumps(str)
    # str = j['ip']
    # print str
