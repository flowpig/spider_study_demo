#!/usr/bin/env python
#-*- coding:utf-8 -*-
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'spider_goods','-a','keyword=iphone8'])