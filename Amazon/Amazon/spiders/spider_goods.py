# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from Amazon.items import AmazonItem

from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        """
        源码入口
        :param args:
        :param opts:
        :return:
        """
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()



# 开始爬虫只有第一页，后来发现params参数写多了，最后只留下field-keywords就没问题了
class SpiderGoodsSpider(scrapy.Spider):
    name = 'spider_goods'
    allowed_domains = ['www.amazon.cn']
    def __init__(self,keyword=None,*args,**kwargs):
        super(SpiderGoodsSpider,self).__init__(*args,**kwargs)
        self.keyword = keyword

    def start_requests(self):
        url = 'https://www.amazon.cn/s/ref=nb_sb_noss_1?'
        params = {
            'field-keywords': self.keyword
        }
        url = url + urlencode(params,encoding='utf-8')
        yield scrapy.Request(url,callback=self.parse_index)

    def parse_index(self, response):
        '''解析索引页'''
        detail_urls = response.xpath('//*[contains(@id,"result_")]/div/div[3]/div[1]/a/@href').extract()
        # print(detail_urls)
        for url in detail_urls:
            yield scrapy.Request(url,callback=self.parse_detail)

        next_page_url = response.urljoin(response.xpath('//*[@id="pagnNextLink"]/@href').extract_first())
        # print(next_page_url)
        yield scrapy.Request(next_page_url,callback=self.parse_index)

    def parse_detail(self,response):
        '''解析商品详情页'''
        item = AmazonItem()
        item['goods_name'] = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
        item['goods_price'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first().strip()
        print(item)

# class SpiderGoodsSpider(scrapy.Spider):
#     name = 'spider_goods'
#     allowed_domains = ['www.amazon.cn']
#     # start_urls = ['http://www.amazon.cn/']
#     def __init__(self,keyword=None,*args,**kwargs):
#         super(SpiderGoodsSpider,self).__init__(*args,**kwargs)
#         self.keyword=keyword
#
#     def start_requests(self):
#         url='https://www.amazon.cn/s/ref=nb_sb_noss_1?'
#         parmas={
#             'field-keywords': self.keyword
#         }
#         url=url+urlencode(parmas,encoding='utf-8')
#
#         yield scrapy.Request(url,callback=self.parse_index)
#
#     def parse_index(self, response):
#         # print('=parse===========>',response.url)
#
#         #拿到详情页的链接
#         urls=response.xpath('//*[contains(@id,"result_")]/div/div[3]/div[1]/a/@href').extract()
#         # print('=parse===========>',urls)
#         print(urls)
#         for url in urls:
#             yield scrapy.Request(url,callback=self.parse_detail) #请求详情页
#
#         #拿到下一页的url
#         next_url=response.urljoin(response.xpath('//*[@id="pagnNextLink"]/@href').extract_first())
#         yield scrapy.Request(next_url,callback=self.parse_index)
#
#     def parse_detail(self,response):
#         # print('=详情页===========>',response.url)
#         #编辑items.py
#         #导入AmazonItem类
#         #item=AmazonItem()
#         #解析response.text 拿到商品名，价钱，快递方
#
#         item=AmazonItem()
#         item['goods_name']=response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
#         item['goods_price']=response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first().strip()
#         # item['delivery_mode']=
#
#         print(item)