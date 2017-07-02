#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import base64

class Utility():
    @staticmethod
    def writeArticleToFile(a):
        file = open('./data/'+a['title']+'.html', 'wb')
        try:
            file.write('<!doctype html>')
            file.write('<html>')
            file.write('<head>')
            file.write('<title>'+ str(a['title'])+'</title>')
            file.write('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">')
            file.write('<meta http-equiv="X-UA-Compatible" content="IE=edge">')
            file.write('<meta name="keywords" content="html,前端">')
            file.write('<meta name="description" content="最好用的前端知识库">')
            file.write('<link href="./css/reset.css" rel="stylesheet" type="text/css">')


            file.write('<body/>')
            file.write('<p> title = ' + str(a['title']) + '</p>')
            file.write('<p> date = ' + str(a['date']) + '</p>')
            file.write('<p> author = ' + str(a['author']) + '</p>')
            file.write('<p> account = ' + str(a['account']) + '</p>')
            file.write('<p> accountId =' + str(a['accountId']) + '</p>')
            file.write(a['content'])
            file.write('</body>')

            file.write('</html>')
        finally:
            file.close()

    @staticmethod
    def listToStr(strList):
        s = ''
        for c in strList:
            s += c
        return s

    @staticmethod
    def getPicFromUrl(url,filename):
        urllib.urlretrieve(url, filename=filename, reporthook=None, data=None)

    @staticmethod
    def convertPicToBase64(filename):
        f=open(filename,'rb') #二进制方式打开图文件
        ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
        f.close()
        return ls_f
