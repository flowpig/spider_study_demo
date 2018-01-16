#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
#twisted基本用法
from twisted.web.client import getPage,defer
from twisted.internet import reactor

def all_done(arg):
    # print(arg)
    reactor.stop()

def callback(res):
    print(res)
    return 1

defer_list=[]
urls=[
    'http://www.baidu.com',
    'http://www.bing.com',
    'https://www.python.org',
]
for url in urls:
    obj=getPage(url.encode('utf-8'),)
    obj.addCallback(callback)
    defer_list.append(obj)

defer.DeferredList(defer_list).addBoth(all_done)

reactor.run()
'''


#twisted的getPage的详细用法   
from twisted.internet import reactor
from twisted.web.client import getPage
import urllib.parse

def one_done(arg):
    print(arg)
    reactor.stop()

post_data = urllib.parse.urlencode({'check_data':'adf'})
post_data = bytes(post_data,encoding='utf-8')
headers = {b'Content-Type': b'application/x-www-form-urlencoded'}
response = getPage(bytes('http://dig.chouti.com/login', encoding='utf8'),
                   method=bytes('POST', encoding='utf8'),
                   postdata=post_data,
                   cookies={},
                   headers=headers
                   )
response.addBoth(one_done)

reactor.run()
