#!/usr/bin/env python
#-*- coding:utf-8 -*-


# from scrapy import signals
# from scrapy.exceptions import NotConfigured
#
# class MyExtension(object):
#     def __init__(self, crawler):
#         self.crawler = crawler
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         ext = cls(crawler)
#
#         crawler.signals.connect(ext.spider_opened, signals.spider_opened)
#         crawler.signals.connect(ext.spider_closed, signals.spider_closed)
#         return ext
#
#     def spider_opened(self, spider):
#         print('open')
#
#     def spider_closed(self, spider):
#         print('close')

from scrapy import signals

class MyExtension(object):

    def __init__(self,crawler):
        self.crawler = crawler
        self.items = 0
        self.requests_ok = 0

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.response_received, signal=signals.response_received)
        return ext

    def spider_opened(self, spider):
        print("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        print("closed spider %s" % spider.name)

    def response_received(self,response, request, spider):
        if response.status == 200:
            self.requests_ok+=1
        if self.requests_ok % 50 == 0:
            print("response_ok 50 url is %s"%(response.url))

    def item_scraped(self, item, spider):
        self.items+= 1
        if self.items %500 == 0:
            print("items 500 item_id is %s"%(item["shop_id"]))