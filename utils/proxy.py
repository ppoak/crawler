import pandas as pd
import base64
import requests


def get_ip_pool(pages: int) -> list:
    proxy_base_url = "http://ip.yqie.com/proxygaoni/index"
    proxy_url = [proxy_base_url + ".htm"] + \
        [proxy_base_url + f"_{p}" + ".htm" for p in range(2, pages)]
    ip_pool = pd.DataFrame()
    for i, pu in enumerate(proxy_url):
        print(f"acquiring page \33[44m{i+1}\33[0m ...\r", end='')
        data = pd.read_html(pu)[0]
        data["免费代理 ip"] = data["免费代理 ip"].apply(
            lambda x: str(base64.b64decode(x.split('"')[1]), "utf-8"))
        ip_pool = ip_pool.append(data, ignore_index=True)

    return ip_pool


def filter_available(ip_pool: list, timeout: float = 1.0) -> list:
    ip_pool_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    available_ip = []
    for i in ip_pool.index:
        ip = {
            ip_pool.loc[i, "免费代理类型"].lower(): ip_pool.loc[i, "免费代理类型"].lower() + "://" + ip_pool.loc[i, str(base64.b64decode("5YWN6LS55Luj55CGIGlw"), "utf-8")] + ":" + str(ip_pool.loc[i, str(base64.b64decode("5Luj55CG56uv5Y+j"), "utf-8")])
        }
        ip_pool_list.append(ip)
        try:
            res = requests.get("http://baidu.com",
                               headers=headers, timeout=timeout)
            res.raise_for_status()
            available_ip.append(ip)
            print(
                f"\33[44m{ip_pool.loc[i, '免费代理 ip']}:{ip_pool.loc[i, '代理端口']}\33[0m\t\33[32mavailable\33[0m")
        except:
            print(
                f"\33[44m{ip_pool.loc[i, '免费代理 ip']}:{ip_pool.loc[i, '代理端口']}\33[0m\t\33[31munavailable\33[0m")

    return available_ip


def get_ip_pool_and_filter(pages: int = 5, timeout: float = 1.0) -> list:
    '''获取可用代理ip池，npages越大，可用ip越多，
    但相应的测试速度也就越慢，
    最大ip池页面数参考http://ip.yqie.com/proxygaoni/index.htm，
    目前最大可用页面为3423页
    '''
    return filter_available(get_ip_pool(pages), timeout=timeout)


if __name__ == '__main__':
    '''下面是一个使用实例，对于多线程任务+ip代理池的处理
    1. 获取可用IP代理
    '''
    from multiprocessing import Pool, Manager
    import random
    from retry import retry

    @retry
    def get_data(data_container, proxies, **kwargs):
        res = requests.get(kwargs['url'], headers=kwargs['headers'], params=kwargs['params'],
                           timeout=kwargs['timeout'], proxies=random.choice([proxies]))
        res.raise_for_status()
        result = res.text  # do something
        data_container.append(result)
        # data_container["result"] = result

    proxies = get_ip_pool_and_filter()
    data_container = Manager().list()
    pool = Pool(processes=8)
    for i in range(10):
        pool.apply_async(get_data, args=(data_container, proxies))
    pool.close()
    pool.join()

    # continue with data_container ...