import requests
import time

def download_one(url):
    resp = requests.get(url)
    print('Read {} from {}'.format(len(resp.content), url))
    
def download_all(sites):
    for site in sites:
        download_one(site)

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

