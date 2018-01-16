#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
gevent实现基于greenlet
gevent.sleep()意思是当检测到一个greenlet无执行(通常遇到I/O阻塞停止执行)时，
会执行循环(loop)的下一个greenlet。相当于这里sleep只是模拟I/O。
'''

import gevent
import time

def foo():
    print("running in foo")
    gevent.sleep(2)
    # gevent.sleep(5)
    print("switch to foo again")

def bar():
    print("switch to bar")
    gevent.sleep(5)
    print("switch to bar again")

start = time.time()

#joinall的意思是等待所有的greenlet任务都完成(类似与多线程的join方法|主线程等待join的线程执行完成才结束)
#spawn的意思是创建greenlet事件对象绑定函数并start执行事件
gevent.joinall(
    [gevent.spawn(foo),
     gevent.spawn(bar)]
)

print(time.time() - start)