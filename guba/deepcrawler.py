import random
import requests
import pandas as pd
import datetime
from lxml import etree
from retry import retry
from multiprocessing import Pool, Manager


def get_proxy_pool():
    proxy_pool = 
    
class PageCrawler():

    root_site = "http://guba.eastmoney.com"
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
            }
    today = datetime.datetime.today()
    year = today.year
    month = today.month

    def __init__(self, code: str, page: int, proxy_pool: list = None):
        self.code = code
        self.page = page
        self.proxy_pool = proxy_pool
    
    def overview_info(self, shallow: bool = False):
        url = f"{self.root_site}/list,{self.code},f_{self.page}.html"
        random.shuffle(self.proxy_pool)
        for try_times, proxy in enumerate(self.proxy_pool):
            try:
                res = requests.get(url, headers=self.headers, proxies=proxy, timeout=2, allow_redirects=False)
                res.raise_for_status()
                html = etree.HTML(res.text)

                self.read = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[1]/text()')
                self.comments = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[2]/text()')
                self.title = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[3]/a/text()')
                self.href = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[3]/a/@href')
                self.author = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[4]/a/font/text()')
            
                if shallow:
                    self.datetime = html.xpath('//*[@id="articlelistnew"]/div[not(@class="dheader")]/span[5]/text()')
                    if int(max(self.datetime)[:2]) > self.month:
                        self.datetime = list(map(lambda x: str(self.year - 1) + '-' + x, self.datetime))
                    else:
                        self.datetime = list(map(lambda x: str(self.year) + '-' + x, self.datetime))
                
                print(f'Getting page {self.page} ... no. {try_times + 1} times try, success!')
                return
            
            except:
                print(f'Getting page {self.page} ... no. {try_times + 1} times try, failed!')

    def shallow_run(self, data_container: list):
        self.overview_info(shallow=True)
        data = pd.DataFrame({
            "read": self.read,
            "comments": self.comments,
            "title": self.title,
            "href": self.href,
            "author": self.author,
            "datetime": pd.to_datetime(self.datetime)
        })
        data_container[str(self.page)] = data


    def _detail_info(self, ref: str):
        if ref.startswith('//'):
            self.content.append(None)
            self.datetime.append(None)
            self.source.append(None)
        else:
            random.shuffle(self.proxies)
            for try_times, proxy in enumerate(self.proxies):
                try:
                    url = self.root_site + ref
                    res = requests.get(url, headers=self.headers, proxies=proxy, timeout=2, allow_redirects=False)
                    res.raise_for_status()
                    html = etree.HTML(res.text)

                    self.content.append(''.join(html.xpath('//*[@id="zwconbody"]//text()').replace(r'\r\n', '').strip()))
                    datetime_and_source = html.xpath('//*[@id="zwconttb"]/div[@class="zwfbtime"]/text()')
                    if datetime_and_source:
                        self.datetime += list(map(lambda x: ' '.join(x.split(' ')[1:-1]).replace(r'\r\n', '').strip(), datetime_and_source))
                        self.source += list(map(lambda x: x.split(' ')[-1], datetime_and_source))
                    else:
                        self.datetime.append(None)
                        self.source.append(None)
                except:
                    print(f'Getting detail info of page {self.page} ... no. {try_times + 1} times try, failed!')

    def detail_info(self):
        self.content = []
        self.datetime = []
        self.source = []
        if not self.href:
            raise ValueError('please use ovreview_info method first')
        for ref in self.href:
            self._detail_info(ref)

    def run(self):
        self.overview_info()
        self.detail_info()
        data = pd.DataFrame({
            "read": self.read,
            "comments": self.comments,
            "title": self.title,
            "href": self.href,
            "author": self.author,
            "content": self.content,
            "datetime": pd.to_datetime(self.datetime),
            "source": self.source
        })
        return data

def run(code, page, proxy_pool, data_container):
    crawler = PageCrawler(code, page, proxy_pool)
    data_container
    

if __name__ == "__main__":
    import time

    # proxy_pool = get_ip_new(30)
    # proxy_pool = [{}]
    # stocks = {'601012': 1237, '600438': 932, '300274': 502, '002129': 473, '600089': 973, 
    #  '300450': 170, '002459': 229, '688599': 122, '603806': 108, '601877': 272}
    # p = Pool(processes=8)
    # for code, end_page, in stocks.items():
    #     data_container = Manager().dict()
    #     start_time = time.time()
    #     for page in range(1, end_page + 1):
    #         crawler = PageCrawler(code, page, proxy_pool)
    #         p.apply_async(func=crawler.shallow_run, args=(data_container,))
    #     p.close()
    #     p.join()
    #     end_time = time.time()
    #     print(f'601012 time usage: {round(end_time - start_time, 2)}s')
    
    #     result = pd.concat(list(data_container.values()), axis=0)
    #     result = result.set_index('datetime').sort_index()
    #     result.to_csv(f'data/{code}.csv')
