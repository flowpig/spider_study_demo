#!/usr/bin/env python
#-*- coding:utf-8 -*-

from gevent import monkey;monkey.patch_all()
import gevent
import requests

def get_page(url):
    print("GET:%s" %url)
    response = requests.get(url)
    print(url,len(response.text))
    return len(response.text)

g1=gevent.spawn(get_page,'https://www.python.org/doc')
g2=gevent.spawn(get_page,'http://www.163.com')
g3=gevent.spawn(get_page,'https://www.openstack.org')
gevent.joinall([g1,g2,g3,])
print(g1.value,g2.value,g3.value) #拿到返回值

#协程池
# from gevent.pool import Pool
# pool=Pool(2)
# g1=pool.spawn(get_page,'https://www.python.org/doc')
# g2=pool.spawn(get_page,'http://www.163.com')
# g3=pool.spawn(get_page,'https://www.openstack.org')
# gevent.joinall([g1,g2,g3,])
# print(g1.value,g2.value,g3.value) #拿到返回值