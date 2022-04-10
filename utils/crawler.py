import time
import random
import requests
import json
from lxml import etree
from bs4 import BeautifulSoup


class ProxyCrawler(object):
    
    def __init__(self, url, **kwargs):
        self.url = url
        self.headers = kwargs.get('headers', self.header())
        self.proxies = kwargs.get('proxies', {})
        self.timeout = kwargs.get('timeout', 2)
        self.retry = kwargs.get('retry', -1)
        self.retry_delay = kwargs.get('retry_delay', 0)
        self.kwargs = {}
        for key, values in kwargs.items():
            if key not in ['headers', 'proxies', 'timeout', 'retry', 'retry_delay']:
                self.kwargs[key] = values

    def header(self):
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            ]
        base_header = {
            "User-Agent": random.choice(ua_list),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        return base_header
    
    def get(self):
        if isinstance(self.proxies, dict):
            self.proxies = [self.proxies]
        random.shuffle(self.proxies) 
        if self.retry == -1:
            self.retry = len(self.proxies)
        for try_times, proxy in enumerate(self.proxies):
            if try_times + 1 <= self.retry:
                try:
                    response = requests.get(self.url, headers=self.headers, proxies=proxy, **self.kwargs)
                    response.raise_for_status()
                    self.response = response
                    print(f'[+] {self.url}, try {try_times + 1}/{self.retry}')
                    return self
                except Exception as e:
                    print(f'[-] [{e}] {self.url}, try {try_times + 1}/{self.retry}')
                    time.sleep(self.retry_delay)

    def post(self):
        if isinstance(self.proxies, dict):
            self.proxies = [self.proxies]
        random.shuffle(self.proxies) 
        if self.retry == -1:
            self.retry = len(self.proxies)
        for try_times, proxy in enumerate(self.proxies):
            if try_times + 1 <= self.retry:
                try:
                    response = requests.post(self.url, headers=self.headers, proxies=proxy, **self.kwargs)
                    response.raise_for_status()
                    self.response = response
                    print(f'[+] {self.url}, try {try_times + 1}/{self.retry}')
                    return self
                except Exception as e:
                    print(f'[-] [{e}] {self.url}, try {try_times + 1}/{self.retry}')
                    time.sleep(self.retry_delay)

    def get_async(self, container: dict):
        if isinstance(self.proxies, dict):
            self.proxies = [self.proxies]
        random.shuffle(self.proxies) 
        if self.retry == -1:
            self.retry = len(self.proxies)
        for try_times, proxy in enumerate(self.proxies):
            if try_times + 1 <= self.retry:
                try:
                    response = requests.get(self.url, headers=self.headers, proxies=proxy, **self.kwargs)
                    response.raise_for_status()
                    self.response = response
                    container[self.url] = self.process()
                    print(f'[+] {self.url}, try {try_times + 1}/{self.retry}')
                    break
                except Exception as e:
                    print(f'[-] [{e}] {self.url}, try {try_times + 1}/{self.retry}')
                    time.sleep(self.retry_delay)

    def post_async(self, container: dict):
        if isinstance(self.proxies, dict):
            self.proxies = [self.proxies]
        random.shuffle(self.proxies) 
        if self.retry == -1:
            self.retry = len(self.proxies)
        for try_times, proxy in enumerate(self.proxies):
            if try_times + 1 <= self.retry:
                try:
                    response = requests.post(self.url, headers=self.headers, proxies=proxy, **self.kwargs)
                    response.raise_for_status()
                    self.response = response
                    container[self.url] = self.process()
                    print(f'[+] {self.url}, try {try_times + 1}/{self.retry}')
                    break
                except Exception as e:
                    print(f'[-] [{e}] {self.url}, try {try_times + 1}/{self.retry}')
                    time.sleep(self.retry_delay)

    def process(self):
        raise NotImplementedError

    @property
    def etree(self):
        return etree.HTML(self.response.text)

    @property
    def json(self):
        return json.loads(self.response.text)
    
    @property
    def soup(self):
        return BeautifulSoup(self.response.text, 'lxml')

if __name__ == '__main__':
    html = ProxyCrawler('http://guba.eastmoney.com/list,000564,f_1.html').get().etree
    res = html.xpath('//*[@id="articlelistnew"]/div[2]/span[3]/a/text()')
    print(res)