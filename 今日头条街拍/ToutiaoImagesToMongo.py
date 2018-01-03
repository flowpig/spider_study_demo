#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import os
from urllib.parse import urlencode
import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError,RequestException
import re
from multiprocessing import Pool
from hashlib import md5
from json.decoder import JSONDecodeError
from toutiaoconfig import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'format': 'json',
        'keyword': keyword,
        'offset': offset,
    }
    params = urlencode(data)
    base = 'http://www.toutiao.com/search_content/'
    url = base + '?' + params
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Error occurred')
        return None


def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def parse_page_index(text):
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Error occurred')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('title')
    title = result[0].get_text() if result else ''
    images_list = re.findall(r'http://p.*?&quot;',html,re.S)
    for image in images_list:download_image(image.strip('&quot;'))
    if images_list:
            return {
                'title': title,
                'url': url,
                'images': images_list
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Successfully Saved to Mongo', result)
        return True
    return False


def main(offset):
    text = get_page_index(offset, KEYWORD)
    urls = parse_page_index(text)
    for url in urls:
        html = get_page_detail(url)
        result = parse_page_detail(html, url)
        if result: save_to_mongo(result)

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()