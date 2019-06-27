# -*- coding:utf-8 -*-
import concurrent.futures
import requests
import threading
import time

def download_one(url):
    resp = requests.get(url)
    print('Read {} from {}'.format(len(resp.content), url))
    return url
    
# 首先调用executor.submit(), 将下载每一个网站的内容放进future队列to_do等待执行。然后
# 是as_completed()函数，在下载完成后输出结果。
def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        to_do = []
        res_li = []
        for site in sites:
            future = executor.submit(download_one, site)
            to_do.append(future)
        for future in concurrent.futures.as_completed(to_do):
            res = future.result()
            res_li.append(res)
        print(res_li)

def main():
    sites = [
        'http://www.w3school.com.cn/html/index.asp',
        'http://www.w3school.com.cn/php/index.asp',
        'http://www.w3school.com.cn/sql/index.asp',
        'http://www.w3school.com.cn/asp/index.asp',
        'http://www.w3school.com.cn/ado/index.asp',
        'http://www.w3school.com.cn/xml/index.asp',
        'http://www.w3school.com.cn/dtd/index.asp',
        'http://www.w3school.com.cn/html5/index.asp',
        'http://www.w3school.com.cn/xhtml/index.asp',
        'http://www.w3school.com.cn/css/index.asp',
        'http://www.w3school.com.cn/css3/index.asp',
        'http://www.w3school.com.cn/json/index.asp',
        'http://www.w3school.com.cn/dhtml/index.asp',
        'http://www.w3school.com.cn/xpath/index.asp',
        'http://www.w3school.com.cn/svg/index.asp',
        'https://www.cnblogs.com/',
        'https://www.jianshu.com/',
        'http://www.chinaz.com/'
    ]
    start_time = time.perf_counter()
    download_all(sites)
    end_time = time.perf_counter()
    print('Download {} sites in {} seconds'.format(len(sites), end_time - start_time))
    
if __name__ == '__main__':
    main()

