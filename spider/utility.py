#!/usr/bin/python
# -*- coding:utf-8 -*-


class Utility():
    @staticmethod
    def writeArticleToFile(a):
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

    @staticmethod
    def listToStr(strList):
        s = ''
        for c in strList:
            s += c
        return s
