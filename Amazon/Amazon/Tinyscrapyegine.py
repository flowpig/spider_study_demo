#!/usr/bin/env python
#-*- coding:utf-8 -*-

import types
from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor
from queue import Queue


class Request(object):
    """
    封装请求相关信息
    """
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback
        self.priority = 0


class HttpResponse(object):
    """
    封装相应相关信息
    """
    def __init__(self, content, request):
        self.content = content
        self.request = request


class Scheduler(object):
    """
    任务调度器
    """
    def __init__(self):
        self.q = Queue()

    def open(self):
        pass

    def next_request(self):
        try:
            request = self.q.get(block=False)
        except Exception as e:
            request = None

        return request

    def enqueue_request(self, request):
        self.q.put(request,block=False)

    def size(self):
        return self.q.qsize()


class CallLaterOnce(object):
    """
    用于封装：执行下次nextcall.schedule()时，可以携带spider参数
    """
    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._kw = kw
        self._call = None

    def schedule(self, delay=0):
        if self._call is None:
            self._call = reactor.callLater(delay, self)

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self):
        self._call = None
        return self._func(*self._a, **self._kw)


class ExecutionEngine(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.nextcall = None
        self.crawlling = []
        self.max = 5
        self._closewait = None
        self.scheduler = None

    def get_response(self, content, request):
        response = HttpResponse(content, request)
        gen = request.callback(response)
        if isinstance(gen, types.GeneratorType):
            for req in gen:
                req.priority = request.priority + 1
                self.scheduler.enqueue_request(req)

    def _next_request(self, spider):
        if self.scheduler.size() == 0 and len(self.crawlling) == 0:
            self._closewait.callback(None)
        if len(self.crawlling) >= 5:
            return
        while len(self.crawlling) < 5:
            req = self.scheduler.next_request()
            if not req:
                return
            d = getPage(req.url.encode('utf-8'))
            self.crawlling.append(d)
            d.addCallback(self.get_response, req)
            d.addCallback(lambda _,d:self.crawlling.remove(d), d)
            d.addCallback(lambda _: self.nextcall.schedule())

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        self.scheduler = Scheduler()

        flag = True
        while flag:
            try:
                req = next(start_requests)
                self.scheduler.enqueue_request(req)
            except StopIteration as e:
                flag = False
        self.nextcall = CallLaterOnce(self._next_request, spider)
        self.nextcall.schedule()
        yield None

    @defer.inlineCallbacks
    def start(self):
        self._closewait = defer.Deferred()
        yield self._closewait


class Crawler(object):
    def __init__(self, spider_cls_path, settings):
        self.spider_cls_path = spider_cls_path
        self.settings = settings

        self.spider = None
        self.engine = None

    def _create_spider(self):
        """
        创建爬虫对象
        :return: 
        """
        module_path, cls_name = self.spider_cls_path.rsplit('.', maxsplit=1)
        import importlib

        m = importlib.import_module(module_path)
        cls = getattr(m, cls_name)
        return cls()

    def _create_engine(self):
        """
        创建引擎
        :return: 
        """
        return ExecutionEngine(self)

    @defer.inlineCallbacks
    def crawl(self):
        """
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.spider = self._create_spider()
        self.engine = self._create_engine()
        start_requests = iter(self.spider.start_requests())
        yield self.engine.open_spider(self.spider, start_requests)
        yield self.engine.start()


class CrawlerProcess(object):
    def __init__(self, settings):
        self.settings = settings
        self._active = set()
        self.crawlers = set()

    def crawl(self, spider_cls_path):
        """
        创建Crawler对象
        :param spider_cls_path: 爬虫spider路径
        :param args: 
        :param kwargs: 
        :return: 
        """
        crawler = Crawler(spider_cls_path, self.settings)
        d = crawler.crawl()
        self._active.add(d)

        def _done(result):
            self.crawlers.discard(crawler)
            self._active.discard(d)
            return result

        return d.addBoth(_done)

    def start(self):
        """
        所有爬虫开始工作
        :return: 
        """
        dl = defer.DeferredList(self._active)
        dl.addBoth(self._stop_reactor)

        reactor.run()

    def _stop_reactor(self, _=None):
        """
        爬虫爬去数据完毕
        :return: 
        """
        reactor.stop()


class Commond(object):
    def __init__(self):
        self.crawl_process = CrawlerProcess({})

    def run(self):
        spider_path_list = [
            "spider.chouti.ChoutiSpider",
            "spider.cnblogs.CnblogsSpider",
        ]
        for spider_cls_path in spider_path_list:
            self.crawl_process.crawl(spider_cls_path)

        self.crawl_process.start()


if __name__ == '__main__':
    cmd = Commond()
    cmd.run()
