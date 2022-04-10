import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP


def senti_ratio(data):
    # if data.empty:
    #     return np.nan
    score = data.apply(lambda x: SnowNLP(x).sentiments)
    pos = score[score >= 0.5]
    neg = score[score < 0.5]
    return pos.sum() / neg.sum()

def senti_ratio_weighted(data):
    # if data.empty:
    #     return np.nan
    score = data['title'].apply(lambda x: SnowNLP(x).sentiments)
    pos = score[score >= 0.5] * (data['read'] + data['comments'])
    neg = score[score < 0.5] * (data['read'] + data['comments'])
    return pos.sum() / neg.sum()

stocks = ['601012', '600438', '300274', '002129', '600089', 
        '300450', '002459', '688599', '603806', '601877']
data = []
for stock in stocks:
    data.append(pd.read_csv(f'data/{stock}.csv', index_col=0, parse_dates=True))
data = pd.concat(data, axis=0)
data = data.loc[:"2022-04-10"].sort_index()
data.loc[:, "read"] = data.loc[:, "read"].replace('万', 'e4', regex=True).apply(lambda x: int(eval(str(x))))
price = pd.read_excel('data/光伏指数收盘价.xlsx', index_col=0, parse_dates=True)
price = price.loc["2021-04-29":"2022-04-10"].rolling(window=7).mean()
price = price['光伏产业931151.CSI']

daily_title = data['title'].resample('d').count()
daily_title_ma7 = daily_title.rolling(window=7).mean()
daily_title_ma14 = daily_title.rolling(window=14).mean()
daily_title = pd.concat([daily_title, daily_title_ma7, daily_title_ma14, price], axis=1)

daily_read_comments = (data['read'] + data['comments']).resample('d').sum()
daily_read_comments_ma7 = daily_read_comments.rolling(window=7).mean()
daily_read_comments_ma14 = daily_read_comments.rolling(window=14).mean()
daily_read_comments = pd.concat([daily_read_comments, daily_read_comments_ma7, daily_read_comments_ma14, price], axis=1)

ratio = data['title'].resample('d').apply(senti_ratio)
ratio_ma7 = ratio.rolling(window=7).mean()
ratio_ma14 = ratio.rolling(window=14).mean()
ratio = pd.concat([ratio, ratio_ma7, ratio_ma14, price], axis=1)

ratio_weighted = data.loc[:, ['title', 'read', 'comments']].resample('d').apply(senti_ratio_weighted)
ratio_weighted_ma7 = ratio_weighted.rolling(window=7).mean()
ratio_weighted_ma14 = ratio_weighted.rolling(window=14).mean()
ratio_weighted = pd.concat([ratio_weighted, ratio_weighted_ma7, ratio_weighted_ma14, price], axis=1)

with pd.ExcelWriter('data/result.xlsx') as writer:
    daily_title.to_excel(writer, sheet_name='每日发帖数')
    daily_read_comments.to_excel(writer, sheet_name='每日评论阅读数')
    ratio.to_excel(writer, sheet_name='情绪指数比例')
    ratio_weighted.to_excel(writer, sheet_name='加权情绪指数比例')

# daily_title = data['title'].resample('d').count().rolling(window=14).mean()
# plt.figure(figsize=(12, 8))
# plt.bar(daily_title.index, daily_title.values)
# plt.twinx()
# plt.plot(price.index, price['光伏866023.WI'], color='green', label='866023.WI')
# plt.plot(price.index, price['光伏产业931151.CSI'], color='red', label='931151.CSI')
# plt.title('Daily title numbers (moving average 14d)')
# plt.legend()
# plt.savefig('daily_title.png')

# daily_read_comments = (data['read'] + data['comments']).resample('d').sum().rolling(window=14).mean()
# plt.figure(figsize=(12, 8))
# plt.bar(daily_read_comments.index, daily_read_comments.values)
# plt.twinx()
# plt.plot(price.index, price['光伏866023.WI'], color='green', label='866023.WI')
# plt.plot(price.index, price['光伏产业931151.CSI'], color='red', label='931151.CSI')
# plt.title('Daily read and comments numbers (moving average 14d)')
# plt.legend()
# plt.savefig('daily_read_comments.png')

# ratio = data['title'].resample('d').apply(senti_ratio).rolling(window=7).mean()
# plt.figure(figsize=(12, 8))
# plt.plot(ratio.index, ratio.values)
# plt.twinx()
# plt.plot(price.index, price['光伏866023.WI'], color='green', label='866023.WI')
# plt.plot(price.index, price['光伏产业931151.CSI'], color='red', label='931151.CSI')
# plt.title('Sentiment ratio (moving average 7d)')
# plt.legend()
# plt.savefig('sentiment_ratio.png')

# ratio = data.loc[:, ['title', 'read', 'comments']].resample('d').apply(senti_ratio_weighted).rolling(window=7).mean()
# plt.figure(figsize=(12, 8))
# plt.plot(ratio.index, ratio.values)
# plt.twinx()
# plt.plot(price.index, price['光伏866023.WI'], color='green', label='866023.WI')
# plt.plot(price.index, price['光伏产业931151.CSI'], color='red', label='931151.CSI')
# plt.title('Sentiment ratio weighted (moving average 7d)')
# plt.legend()
# plt.savefig('sentiment_ratio_weighted.png')
