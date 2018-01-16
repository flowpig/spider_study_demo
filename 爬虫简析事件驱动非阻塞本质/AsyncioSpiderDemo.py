#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
asyncio模块可以帮助我们检查I/O(只能是网络I/O),实现应用程序级别的切换，
asyncio模块只能发tcp级别的请求，不能发http请求，因此，在我们需要发送
http请求的时候，需要我们自定义http报头或者直接使用aiohttp模块，这个模块
专门帮我们封装http报头
'''

'''

#便于理解的小Demo
import asyncio

@asyncio.coroutine
def task(task_id,seconds):
    print("%s is start" %task_id)
    yield from asyncio.sleep(seconds)       #只能检测网络IO，检测到I/O后切换到其它任务执行
    print("%s is end" %task_id)

tasks =[task(task_id=1,seconds=3),task(task_id=2,seconds=4)]

loop = asyncio.get_event_loop()     #返回一个asyncio的事件循环
loop.run_until_complete(asyncio.gather(*tasks))     #运行事件循环，直到Future对象完成或者执行异常   def run_until_complete(self, future):
# asyncio.gather(*coros_or_futures)返回:Return a future aggregating results from the given coroutines or futures.
loop.close()        #关闭事件循环

'''

#---------------------------------------------------------------------------------------
'''
使用asyncio发送http报文，自定制http报头
'''

'''
import asyncio

@asyncio.coroutine
def get_page(host,port=80,url='/'):
    #步骤一(IO阻塞):发起tcp连接，是阻塞操作，因此需要yield from
    recv,send = yield from asyncio.open_connection(host,port)

    #步骤二:封装http协议的报头，因为asyncio模块只能封装并发送tcp包，因此这一步需要我们自己封装http协议的包
    request_headers = """GET %s HTTP/1.0\r\nHost:%s\r\n\r\n""" %(url,host)
    # requset_headers="""POST %s HTTP/1.0\r\nHost: %s\r\n\r\nname=egon&password=123""" % (url, host,)
    request_headers = request_headers.encode('utf-8')

    #步骤三(IO阻塞):发送http请求包
    send.write(request_headers)
    yield from send.drain()

    #步骤四（IO阻塞）:接收http协议的响应包
    text = yield from recv.read()

    #其它处理
    print(host,url,text)
    send.close()
    print('----->')
    return len(text)

tasks = [
    get_page(host='www.python.org',url='/doc'),
    get_page(host='www.openstack.org'),
]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
'''
#-----------------------------------------------------------------------------------------------------
'''
使用aiohttp模块帮我们自自定制http报头
'''
import asyncio
import aiohttp

@asyncio.coroutine
def get_page(url):
    print('GET %s' %url)
    response = yield from aiohttp.request('GET',url)
    data = yield from response.read()
    print(url,data)
    response.close()
    return len(data)

tasks=[
    get_page('https://www.python.org/doc'),
    get_page('http://www.163.com'),
    get_page('https://www.openstack.org')
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()