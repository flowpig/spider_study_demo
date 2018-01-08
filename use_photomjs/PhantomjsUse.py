#!/usr/bin/env python
#-*- coding:utf-8 -*-
#coding:utf-8
import unittest
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class seleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.ss = None

    def testEle(self):
        driver = self.driver
        driver.get('https://www.autohome.com.cn/news/1/#liststart')
        # wait = WebDriverWait(driver,10)
        # wait.until(EC.presence_of_element_located((By.ID,'auto-channel-lazyload-article')))
        obj = re.compile(
            r'<li data-artidanchor="\d+".*?href="(?P<link>.*?)".*?class="article-pic"><img src="(?P<img>.*?)".*?<h3>(?P<title>.*?)</h3>.*?<span class="fn-left">(?P<time>.*?)</span>.*?class="icon12 icon12-eye"></i>(?P<visitor>.*?)</em>.*?class="icon12 icon12-infor"></i>(?P<comment>.*?)</em>',
            re.S)
        r = obj.finditer(driver.page_source)
        for i in r:
            print(i.group('link', 'img', 'title', 'time', 'visitor', 'comment'))



    def tearDown(self):
        print('down')

if __name__ == "__main__":
    unittest.main()
