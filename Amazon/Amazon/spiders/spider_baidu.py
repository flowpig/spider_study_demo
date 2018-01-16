# -*- coding: utf-8 -*-
import scrapy


class SpiderBaiduSpider(scrapy.Spider):
    name = 'spider_baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
