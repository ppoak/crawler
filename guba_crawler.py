from multiprocessing import Pool, Manager
from lxml import etree
import pandas as pd
import time
import requests
import random
import base64


def get_ip_pool(pages: int) -> list:
    proxy_base_url = "http://ip.yqie.com/proxygaoni/index"
    proxy_url = [proxy_base_url + ".htm"] + [proxy_base_url + f"_{p}" + ".htm" for p in range(2, pages)]
    ip_pool = pd.DataFrame()
    for i, pu in enumerate(proxy_url):
        print(f"acquiring page {i+1}...")
        data = pd.read_html(pu)[0]
        data[str(base64.b64decode("5YWN6LS55Luj55CGIGlw"), "utf-8")] = data[str(base64.b64decode("5YWN6LS55Luj55CGIGlw"), "utf-8")].apply(lambda x: str(base64.b64decode(x.split('"')[1]), "utf-8"))
        ip_pool = ip_pool.append(data, ignore_index=True)

    return ip_pool

def filter_available(ip_pool: pd.DataFrame) -> list:
    ip_pool_list = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    available_ip = []
    for i in ip_pool.index:
        ip = {
            ip_pool.loc[i, str(base64.b64decode("5YWN6LS55Luj55CG57G75Z6L"), "utf-8")].lower(): ip_pool.loc[i, str(base64.b64decode("5YWN6LS55Luj55CG57G75Z6L"), "utf-8")].lower() + "://" + ip_pool.loc[i, str(base64.b64decode("5YWN6LS55Luj55CGIGlw"), "utf-8")] + ":" + str(ip_pool.loc[i, str(base64.b64decode("5Luj55CG56uv5Y+j"), "utf-8")])
        }
        ip_pool_list.append(ip)
        try:
            res = requests.get("http://baidu.com", headers=headers, timeout=2)
            res.raise_for_status()
            available_ip.append(ip)
            print(f"{ip_pool.loc[i, '免费代理 ip']}:{ip_pool.loc[i, '代理端口']}\tavailable")
        except:
            print(f"{ip_pool.loc[i, '免费代理 ip']}:{ip_pool.loc[i, '代理端口']}\tunavailable")
    return available_ip

def get_comment(process: int, stockid: str, startpage: int, endpage: int, proxies: list, data: dict) -> None:
    print(f"process no. {process + 1} process started...")
    url_template = "http://guba.eastmoney.com/list,{},f_{}.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
    comments = []
    for p in range(startpage, endpage):
        url = url_template.format(stockid, p)
        random.shuffle(proxies)
        proxies_with_noproxies = proxies + [{}]
        for try_times, ip in enumerate(proxies_with_noproxies):
            try:
                if not ip:
                    print(f"attemping page {p}, using {'no proxy':29}, try {try_times + 1}...")
                else:
                    print(f"attemping page {p}, using {list(ip.values())[0]:29}, try {try_times + 1}...")
                res = requests.get(url, headers=headers, proxies=ip, timeout=2)
                res.raise_for_status()
                res.encoding = "utf-8"
                tree = etree.HTML(res.text)
                comm_time = tree.xpath('//*[@id="articlelistnew"]/div/span[5]/text()')
                comm_time.remove('发帖时间')
                comm_content = tree.xpath('//*[@id="articlelistnew"]/div/span[3]/a/text()')
                comment = list(zip(comm_time, comm_content))
                comments += comment
                if not ip:
                    print(f"attemping page {p}, using {'no proxy':29}, try {try_times + 1}...\tsuccess!")
                else:
                    print(f"attemping page {p}, using {list(ip.values())[0]:29}, try {try_times + 1}...\tsuccess!")
                break
            except:
                if not ip:
                    print(f"attemping page {p}, using {'no proxy':29}, try {try_times + 1}...\tfailed!")
                else:
                    print(f"attemping page {p}, using {list(ip.values())[0]:29}, try {try_times + 1}...\tfailed!")

    data[process] = comments


if __name__=='__main__':

    # handle inputs
    stockid = input("input stockid: (default 'zssh000001')\n>>> ")
    pages = input("input pages: (must be integer, default: 1000)\n>>> ")
    proxy_pages = input("input proxy pages: (must be integer, default: 10)\n>>> ")
    processes = input("input processes: (must be integer, default: 4)\n>>> ")

    if not stockid:
        stockid = "zssh000001"
    if not pages:
        pages = 1000
    else:
        pages = int(pages)
    if not proxy_pages:
        proxy_pages = 10
    else:
        proxy_pages = int(proxy_pages)
    if not processes:
        processes = 4
    else:
        processes = int(processes)
    
    # get proxies
    get_proxy_time_start = time.time()
    ip_pool = get_ip_pool(10)
    proxies = filter_available(ip_pool)
    print(f"find {len(proxies)} available, using {time.time() - get_proxy_time_start:.2f}s, load them for crawling comments...")

    # create processing pool and crawl for data
    get_comments_time_start = time.time()
    p = Pool(processes=processes)
    data_dict = Manager().dict()
    for i in range(4):
        startpage = (pages * i) // processes + 1
        endpage = (pages * (i + 1)) // processes + 1
        p.apply_async(get_comment, (i, stockid, startpage, endpage, proxies, data_dict))
    p.close()
    p.join()
    print (f'completed, using {time.time() - get_proxy_time_start:.2f}s, now saving data...')

    # mission completed 
    comments = []
    for v in data_dict.values():
        comments += v
        
    comments = pd.DataFrame(comments, columns=["time", "comment"])
    comments = comments.sort_index()
    comments.to_csv("data/comments.csv", index=False)
    print("saving succeed, saved at `data/comments.csv`")