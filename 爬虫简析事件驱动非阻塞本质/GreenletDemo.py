#!/usr/bin/env python
#-*- coding:utf-8 -*-

from greenlet import greenlet

def foo1():
    print(12)
    gr2.switch()
    print(34)
    gr2.switch()

def foo2():
    print(56)
    gr1.switch()
    print(78)

gr1 = greenlet(foo1)
gr2 = greenlet(foo2)
gr1.switch()