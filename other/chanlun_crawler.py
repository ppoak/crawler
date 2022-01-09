import requests
from bs4 import BeautifulSoup
import time

url = "https://baiyunju.cc/1347"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
para = soup.select(".article-content p")[2:]
href_list = list(map(lambda x: x("a")[0]["href"], para))
title_list = list(map(lambda x: x.text, para))
articles = {}
for i, hrf in enumerate(href_list):
    print(f"getting {i+1} page ... ", end='')
    try:
        r = requests.get(hrf)
        r.raise_for_status()
        article = BeautifulSoup(r.text, 'html.parser')
        article = article.select(".article-content p")[:-1]
        articles[title_list[i]] = list(map(lambda x: x.text, article))
        print("\tsuccess")
        # time.sleep(3)
    except:
        print(f"\tfailed")

with open("chanlun.md", 'w') as fp:
    fp.write("# 缠论\n\n")
    for k, v in articles.items():
        fp.write("## " + k + "\n\n")
        for p in v:
            fp.write(p + "\n\n")
