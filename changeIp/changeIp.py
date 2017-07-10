import urllib2
proxy_support = urllib2.ProxyHandler({'http':'1.31.102.64:80'})
opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
content = urllib2.urlopen('http://192.243.119.61:18080/book').read()
print content
