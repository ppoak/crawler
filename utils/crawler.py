import re
import json
import time
import base64
import random
import requests
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


class ProxyFetcher(object):

    available_proxy_source = [
        'mipu', 'daili66', 'kaixin', 'dieniao', 'kuaidaili',
        'daili11', 'yun', 'xiaohuan', 'mianfei', 'daili89', 'yqie'
    ]
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
    }
    
    def mipu(self):
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
        ]
        result = []
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html_tree = etree.HTML(requests.get(url, headers=self.headers).text)
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if port:
                        result.append({"http": "http://" + '%s:%s' % (ip, port),
                             "https": "https://" + '%s:%s' % (ip, port)})
                except Exception as e:
                    print(e)

    def daili66(self):
        url = "http://www.66ip.cn/mo.php"
        result = []
        resp = requests.get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
        for proxy in proxies:
            result.append({"http": "http://" + proxy, "https": "http://" + proxy})
        return result

    def kaixin(self):
        result = []
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = etree.HTML(requests.get(url, headers=self.headers).text)
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                result.append({"http": "http://" + "%s:%s" % (ip, port),
                            "https": "https://" + "%s:%s" % (ip, port)})
        return result

    def dieniao(self):
        result = []
        url = "https://www.dieniao.com/FreeProxy.html"
        tree = etree.HTML(requests.get(url, headers=self.headers, verify=False).text)
        for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
            ip = "".join(li.xpath('./span[1]/text()')).strip()
            port = "".join(li.xpath('./span[2]/text()')).strip()
            result.append({"http": "http://" + "%s:%s" % (ip, port),
                        "https": "https://" + "%s:%s" % (ip, port)})
        return result

    def kuaidaili(self, page_count=1):
        result = []
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))
                
        for url in url_list:
            tree = etree(requests.get(url, headers=self.headers).text)
            proxy_list = tree.xpath('.//table//tr')
            time.sleep(1)
            for tr in proxy_list[1:]:
                result.append({"http": "http://" + ':'.join(tr.xpath('./td/text()')[0:2]),
                               "https": "http://" + ':'.join(tr.xpath('./td/text()')[0:2])})
        return result

    def daili11(self):
        url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
        try:
            result = []
            resp_json = requests.get(url, headers=self.headers).json()
            for each in resp_json.get("data", []):
                result.append({"http": f'http://{each.get("ip", "")}:{each.get("port", "")}', 
                    "https": f'http://{each.get("ip", "")}:{each.get("port", "")}'})
            return result
        except Exception as e:
            print(e)

    def yun(self):
        result = []
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = requests.get(url, headers=self.headers)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                result.append({"http": "http://" + ":".join(proxy), "https": "http://" + ":".join(proxy)})
        return result

    def xiaohuan(self):
        result = []
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = requests.get(url, headers=self.headers, timeout=10)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                result.append({"http": "http://" + ":".join(proxy), "https": "http://" + ":".join(proxy)})
        return result

    def mianfei(self, page_count=1):
        result = []
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = etree.HTML(requests.get(url, headers=self.headers).text)
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                result.append({"http": "http://" + ":".join(tr.xpath("./td/text()")[0:2]).strip(),
                    "https": "http://" + ":".join(tr.xpath("./td/text()")[0:2]).strip()})
        return result

    def daili89(self):
        result = []
        r = requests.get("https://www.89ip.cn/index_1.html", headers=self.headers, timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            result.append({"http": "http://" + ":".join(proxy), "https": "http://" + ":".join(proxy)})
        return result

    def yqie(self, pages: int = 5):
        proxy_base_url = "http://ip.yqie.com/proxygaoni/index"
        proxy_url = [proxy_base_url + ".htm"] + \
            [proxy_base_url + f"_{p}" + ".htm" for p in range(2, pages)]
        ips = []
        ports = []
        for pu in proxy_url:
            html = etree.HTML(requests.get(pu, headers=self.headers).text)
            ip = html.xpath('//*[@id="GridViewOrder"]/tr/td[2]/script/text()')
            port = html.xpath('//*[@id="GridViewOrder"]/tr/td[3]/text()')
            ip_converted = []
            for i in ip:
                i = i.split('"')[1]
                if '.' in i:
                    ip_converted.append(i)
                else:
                    ip_converted.append(base64.b64decode(i).decode('utf-8'))
            ips += ip_converted
            ports += port
        result = []
        for ip, port in zip(ips, ports):
            result.append({"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"})
        return result

class MyProxyCrawler(ProxyCrawler):
    def process(self):
        return self.etree.xpath('//*[@id="articlelistnew"]/div[2]/span[3]/a/text()')

if __name__ == '__main__':
    from multiprocessing import Pool, Manager
    proxy_pool = ProxyFetcher().yqie(19)
    print(proxy_pool)
    target_list = [f'http://guba.eastmoney.com/list,000564,f_{page}.html' for page in range(1, 101)]
    pool = Pool(processes=8)
    container = Manager().dict()
    for target in target_list:
        pool.apply_async(func=MyProxyCrawler(target, proxies=proxy_pool).get_async, args=(container,))
    pool.close()
    pool.join()
    print(dict(container))
