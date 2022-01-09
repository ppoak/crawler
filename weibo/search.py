#!python -m weibo.search

import os
import re
import time
import random
import requests
import pandas as pd
import matplotlib.pyplot as plt

from typing import Union
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils.beautifulio import *


class Search():
    '''A search crawler engine for weibo
    ====================================

    sample usage:
    >>> from search import Search
    >>> search = Search("西安疫情")
    >>> result = search.run()
    >>> result.to_excel("西安疫情-微博热搜.xlsx", index=False)
    '''

    def __init__(self, keyword: str):
        self.base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}&page_type=searchall&page={}"
        self.headers = {
                "Referer": f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{quote(keyword, 'utf-8')}",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
                }
        self.keyword = keyword.replace('#', '%23')

    def _get_content(self, url, headers):

        def _parse(mblog):
            blog = {
                "created_at": mblog["created_at"],
                "text": re.sub(r'<(.*?)>', '', mblog['text']),
                "id": mblog["id"],
                "link": f"https://m.weibo.cn/detail/{mblog['id']}",                    
                "source": mblog["source"],
                "username": mblog["user"]["screen_name"],
                "reposts_count": mblog["reposts_count"],
                "comments_count": mblog["comments_count"],
                "attitudes_count": mblog["attitudes_count"],
                "isLongText": mblog["isLongText"],
            }
            if blog["isLongText"]:
                headers = {
                    "Referer": f"https://m.weibo.cn/detail/{blog['id']}",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"
                }
                resp = requests.get(f"https://m.weibo.cn/statuses/extend?id={blog['id']}", headers=headers).json()
                blog["full_text"] = resp["data"]["longTextContent"]
            return blog

        # First try to get resources
        res = requests.get(url, headers=headers).json()
        # if it is end
        if res.get("msg"):
            return False

        # if it contains cards
        cards = res["data"]["cards"]
        blogs = []
        for card in cards:
            # find 'mblog' tag and append to result blogs
            if mblog:= card.get("mblog"):
                blog = _parse(mblog)
                blogs.append(blog)
            elif card_group:= card.get("card_group"):
                for cg in card_group:
                    if mblog:= cg.get("mblog"):
                        blog = _parse(mblog)
                        blogs.append(blog)
        return blogs
    
    def _get_full(self):
        page = 1
        result = []
        console.log(f"[red]Start in keyword: {self.keyword}")
        while True:
            console.print(f"Getting [blue]{self.keyword}[/blue], currently at page: [blue]{page}[/blue] ... ")
            url = self.base_url.format(self.keyword, page)
            blogs = self._get_content(url, self.headers)
            if not blogs:
                break
            result.extend(blogs)
            page += 1
            time.sleep(random.randint(5, 8))
        console.log(f"[green]Finished in keyword: {self.keyword}!")
        return result
    
    def _get_assigned(self, pages):
        result = []
        console.log(f"[red]Start in keyword: {self.keyword}")
        for page in track(range(1, pages+1)):
            console.print(f"Getting [blue]{self.keyword}[/blue], currently at page: [blue]{page}[/blue] ... ")
            url = self.base_url.format(self.keyword, page)
            blogs = self._get_content(url, self.headers)
            result.extend(blogs)
            time.sleep(random.randint(5, 8))
        console.log(f"[green]Finished in keyword: {self.keyword}!")
        return result          
    
    def run(self, pages: int = -1):
        if pages == -1:
            result = self._get_full()
        else:
            result = self._get_assigned(pages)
        result = pd.DataFrame(result)
        return result


class HotTopic():
    '''A Second Level Crawler for Hot Topic
    ================================================

    sample usage:
    >>> from search import HotTopic
    >>> search = HotTopic("周深")
    >>> result = search.run()
    >>> result.to_excel("周深-热搜话题.xlsx", index=False)
    '''

    def __init__(self, keyword: str = None, date: str = None):
        if keyword is None and date is not None:
            self.url = f"https://google-api.zhaoyizhe.com/google-api/index/mon/sec?keyword={date}"
        elif keyword is None and date is None:
            self.url = f"https://google-api.zhaoyizhe.com/google-api/index/mon/list"
        elif keyword is not None and date is None:
            self.url = f"https://google-api.zhaoyizhe.com/google-api/index/mon/sec?keyword={keyword}"
    
    def search(self):
        result = requests.get(self.url).json()
        data = result["data"]
        data = pd.DataFrame(data)
        data = data.drop("_id", axis=1)
        return data


class Trend():
    '''A Weibo HotTopic Keyword Search Trend Visualizer
    ====================================================

    sample usage:
    >>> trend = Trend('脱发')
    >>> result = trend.get_data()
    >>> trend.plot()
    '''

    def __init__(self, keyword, frequency: str = "3month"):
        if frequency not in ["3month", "1hour", "24hour", "1month", "1day"]:
            raise ValueError("frequency must be one of '3month', '1hour', '24hour', '1month', '1day'")
        self.keyword = keyword
        self.frequency = frequency
        self.headers = {
            "Host": "data.weibo.com",
            "Origin": "https://data.weibo.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001041) NetType/WIFI Language/zh_CN",
            "Content-Length": "23",
            "Referer": "https://data.weibo.com/index/newindex?visit_type=search"
            }
        word_ids = self._search_for_word()
        console.print(word_ids)
        choice = intprompt.ask("Choice of the word above in order number\n>>> ") - 1
        wid = word_ids[choice]["wid"]
        self.wid = wid
        self.post_params = {
            "wid": wid,
            "dateGroup": frequency
        }

    def _search_for_word(self):
        url = "https://data.weibo.com/index/ajax/newindex/searchword"
        data = {
            "word": f"{self.keyword}"
        }
        res = requests.post(url, data=data, headers=self.headers).json()
        html = BeautifulSoup(res["html"], 'html.parser')
        res = html.find_all('li')
        result = []
        for i, r in enumerate(res):
            result.append(
                {
                    "order": i + 1,
                    "word": r.text,
                    "wid": r.attrs["wid"]
                }
            )
        return result
    
    def get_data(self):
        url = "https://data.weibo.com/index/ajax/newindex/getchartdata"
        res = requests.post(url, data=self.post_params, headers=self.headers).json()
        data = res["data"]
        index = data[0]["trend"]['x']
        index = list(map(lambda x: x.replace("月", '-').replace("日", ''), index))
        volume = data[0]["trend"]['s']
        result = pd.Series(volume, index=index, name="weibo_trend")
        self.data = result
        return result

    def plot(self, save_path=None):
        plt.rcParams['axes.unicode_minus'] = False
        self.data.plot()
        if save_path is not None:
            plt.savefig(save_path)
        else:
            plt.show()


class User():
    '''A User Search Which Provides Fast Search Result In someone's Blog
    ================================================================

    sample usage:
    >>> user = User("央视新闻")
    >>> user.search("社区公告", "weibo/data")
    '''
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.cookie = os.environ["WB_COOKIE"]
        self.base_headers = {
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
        }
        choices = self._get_id()
        console.print(choices)
        choice = intprompt.ask("Choose a user in order number to initialize\n>>> ") - 1
        self.user_id = list(choices[choice].values())[0]["id"]
        self.brief_header = {
            "Cookie": self.cookie,
            "Referer": f"https://weibo.com/u/{self.user_id}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
        }
        self.detail_header = {
            "Cookie": self.cookie,
            "Host": "weibo.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
        }

    def search(self, keywords: Union[list, str], save_dir: str):
        if isinstance(keywords, str):
            keywords = [keywords]
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        base_url = "https://weibo.com/ajax/profile/searchblog"
        for kw in keywords:
            url = base_url + f'?uid={self.user_id}&feature=0&q={kw}'
            console.print(f"Fetching for [blue]{kw}[/blue] ... ")
            brief_data = self._get_brief_content(url)
            need_detail = brief_data.loc[brief_data["是否长文"], "全文链接"]
            if need_detail.shape[0]:
                console.print(f"[green]Successfully get {kw} brief information，getting full text[/green]")
                detail_data = self._get_detail_content(need_detail)
            else:
                console.print(f"[green]Successfully get {kw} brief information，[/green][orange]no need for full text[/orange]")
                detail_data = pd.DataFrame()
            console.print(f"[green]Successfully get {kw} full text[/green]")
            result = pd.concat([brief_data, detail_data], axis=1).drop(["全文链接", "是否长文"], axis=1)
            result.to_excel(f"data/{kw}.xlsx", index=False)
            time.sleep(3)

    def _get_brief_content(self, url):
        page = 1
        long_id = []
        create_time = []
        full_text_link = []
        weibo_link = []
        short_text = []
        repost_num = []
        comments_num = []
        attitudes_num = []
        is_long_text = []
        while True:
            url_with_page = url + '&page=' + str(page)
            res = requests.get(url_with_page, headers=self.brief_header).json()
            total = res["data"]["total"]
            if total == 0:
                break
            info_list = res["data"]["list"]
            long_id += list(map(lambda x: x["mblogid"], info_list))
            create_time += list(map(lambda x: x["created_at"], info_list))
            full_text_link += list(map(lambda x: "https://weibo.com/ajax/statuses/longtext?id=" + x, long_id))
            weibo_link += list(map(lambda x: "https://m.weibo.cn/detail/" + x["idstr"], info_list))
            short_text += list(map(lambda x: x["text_raw"], info_list))
            repost_num += list(map(lambda x: x["reposts_count"], info_list))
            comments_num += list(map(lambda x: x["comments_count"], info_list))
            attitudes_num += list(map(lambda x: x["attitudes_count"], info_list))
            is_long_text += list(map(lambda x: x["isLongText"], info_list))
            page += 1
            time.sleep(random.randint(2, 8))
            console.print(f"Got: [green]{len(long_id)} items[/green]")

        data = pd.DataFrame(zip(
            create_time,
            full_text_link,
            is_long_text,
            weibo_link,
            short_text,
            repost_num,
            comments_num,
            attitudes_num
        ), columns=["创建日期", "全文链接", "是否长文", "原文链接", "原文短文", "转发", "评论", "点赞"])
        return data

    def _get_detail_content(self, url_series):
        contents = []
        for url in track(url_series, description="Getting Detail Information"):
            time.sleep(random.randint(3, 5))
            res = requests.get(url, headers=self.detail_header).json()
            contents.append(res["data"].get("longTextContent", "见短文"))

        data = pd.DataFrame(index=url_series.index, columns=["原文"])
        data["原文"] = contents

        return data

    def _get_id(self):
        base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D{}%26t%3D0&page_type=searchall"
        url = base_url.format(quote(self.user_name, 'utf-8'))
        result = requests.get(url).json()
        people_list = result["data"]["cards"][1]["card_group"]
        description = list(map(lambda x: x["desc1"], people_list))
        fans = list(map(lambda x: x["desc2"], people_list))
        name = list(map(lambda x: x["user"]["screen_name"], people_list))
        ids = list(map(lambda x: x["user"]["id"], people_list))
        result = []
        for i, n in enumerate(name):
            res = {n: {}}
            res[n]["order"] = i + 1
            res[n]["desc"] = description[i]
            res[n]["fans"] = fans[i]
            res[n]["id"] = ids[i]
            result.append(res)
        return result


if __name__ == "__main__":
    search = Search("植发")
    result = search.run()
    result.to_excel("植发-热搜.xlsx", index=False)
    # hot = HotTopic("周深")
    # result = hot.search()
    # print(result)
    # trend = Trend('脱发')
    # result = trend.get_data()
    # trend.plot()
    # user = User("央视新闻")
    # user.search(["头发"], "weibo/data")
