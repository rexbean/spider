# -*- coding=utf-8 -*-
import socket
import urllib2
import re
true_socket = socket.socket

ipbind='115.46.67.12'

def bound_socket(*a, **k):
    sock = true_socket(*a, **k)
    sock.bind((ipbind, 8123))
    return sock

socket.socket = bound_socket

response = urllib2.urlopen('http://www.ip.cn')
html = response.read()
ip=re.search(r'code.(.*?)..code',html)
print ip.group(1)
