# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.core.scheduler import Scheduler
from ..items import DaboItem

class SpiderChoutiSpider(scrapy.Spider):
    name = 'spider_chouti'
    allowed_domains = ['dig.chouti.com']

    def start_requests(self):
        yield Request(url='http://dig.chouti.com/', callback=self.parse, dont_filter=True)
        # return [Request(url='www.renjian.com',callback=self.parse),]
        """
        yield
            生成器 = start_requests()
        return
            可迭代对象 = start_requests()

        迭代器 = iter(生成器,可迭代对象)
        """

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        news_list = hxs.xpath('//*[@id="content-list"]/div[@class="item"]')

        for news in news_list:
            content = news.xpath('.//div[@class="part1"]/a/text()').extract_first().strip()
            url = news.xpath('.//div[@class="part1"]/a/@href').extract_first()
            item = DaboItem(url=url, content=content)
            # print(item)




