import pandas as pd
import numpy as np
import requests
from utils.io import *
from utils.key import *


def active_opdep(date: Union[str, datetime.datetime]) -> pd.DataFrame:
    '''Update data for active oprate department
    --------------------------------------------

    date: str or datetime, the given date
    return: pd.DataFrame, a dataframe containing information on eastmoney
    '''
    date = datetime2str(date)
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "TOTAL_NETAMT,ONLIST_DATE,OPERATEDEPT_CODE",
        "sortTypes": "-1,-1,1",
        "pageSize": 100000,
        "pageNumber": 1,
        "reportName": "RPT_OPERATEDEPT_ACTIVE",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(ONLIST_DATE>='{date}')(ONLIST_DATE<='{date}')"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Referer": "https://data.eastmoney.com/"
    }
    info = _em_active_opdep(date)
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json()['result']['data']
    data = pd.DataFrame(data)
    data = data.rename(columns={
        "OPERATEDEPT_NAME": "opdep_name",
        "ONLIST_DATE": "onlist_date",
        "BUYER_APPEAR_NUM": "buy_num",
        "SELLER_APPEAR_NUM": "sell_num",
        "TOTAL_BUYAMT": "buy_amount",
        "TOTAL_SELLAMT": "sell_amount",
        "TOTAL_NETAMT": "net_amount",
        "BUY_STOCK": "buy_stock_code",
        "SECURITY_NAME_ABBR": "buy_stock_name",
        "OPERATEDEPT_CODE": "opdep_code",
        "OPERATEDEPT_CODE_OLD": "opdep_code_old",
        "ORG_NAME_ABBR": "opdep_abbrname"
    })
    data.onlist_date = pd.to_datetime(data.onlist_date)
    return data

def institution_trade(date: Union[str, datetime.datetime]) -> pd.DataFrame:

    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns' : 'NET_BUY_AMT,TRADE_DATE,SECURITY_CODE',
        'sortTypes' : '-1,-1,1',
        'pageSize' : '100000',
        'pageNumber' : '1',
        'reportName' : 'RPT_ORGANIZATION_TRADE_DETAILS',
        'columns' : 'ALL', 
        'source' : 'WEB',
        'client' :  'WEB', 
        'filter' : f"(TRADE_DATE='{date}')"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Referer": "https://data.eastmoney.com/"
    }
    date = datetime2str(date)
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json()['result']['data']
    data = pd.DataFrame(data)
    
    data = pd.DataFrame(data, columns=[
        'SECUCODE', 
        'SECURITY_NAME_ABBR',
        'TRADE_DATE',
        'CLOSE_PRICE',
        'CHANGE_RATE',
        'BUY_TIMES',
        'SELL_TIMES',
        'BUY_AMT',
        'SELL_AMT',
        'NET_BUY_AMT',
        'ACCUM_AMOUNT',
        'RATIO',
        'TURNOVERRATE',
        'FREECAP',
        'EXPLANATION'
        ])

    data = data.rename(columns={
        'SECUCODE':'code',
        'SECURITY_NAME_ABBR': 'stock_name',
        'TRADE_DATE': 'trade_date',
        'CLOSE_PRICE': 'close_price',
        'CHANGE_RATE': 'change_rate',
        'BUY_TIMES': 'buy_time',
        'SELL_TIMES': 'sell_time',
        'BUY_AMT': 'buy_amount',
        'SELL_AMT': 'sell_amount',
        'NET_BUY_AMT': 'net_buy_amount',
        'ACCUM_AMOUNT': 'accum_amount',
        'RATIO': 'ratio',
        'TURNOVERRATE': 'turnover',
        'FREECAP': 'free_cap',
        'EXPLANATION': 'explanation'
    })

    return data

def institution_holding(date: Union[str, datetime.datetime]) -> pd.DataFrame:
    date = datetime2str(date)
    main_page = 'https://data.eastmoney.com/hsgtcg/InstitutionQueryMore.html'
    res = requests.get(main_page)
    res.raise_for_status()
    institution_list = re.findall(r'var jgList= \[.*\];', res.text)[0].split('=')[1].strip(';')
    institution_list = eval(institution_list)

    result = pd.DataFrame()
    for institution in institution_list:
        name = institution['PARTICIPANT_CODE']
        callbackfunc = 'jQuery1123032132491687413733_1646408202496'
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            'callback': callbackfunc,
            'sortColumns': 'HOLD_DATE',
            'sortTypes': '-1',
            'pageSize': '5000',
            'pageNumber': '1',
            'reportName': 'RPT_MUTUAL_HOLD_DET',
            'columns': 'ALL',
            'source': 'WEB',
            'client': 'WEB',
            'filter': f'(PARTICIPANT_CODE="{name}")' + \
                f'(MARKET_CODE in ("001","003"))(HOLD_DATE=\'{date}\')',
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = eval(res.text.replace('true', 'True').replace('false', 'False').\
            replace('null', 'np.nan').replace(callbackfunc, '')[1:-2])
        if data['result'] is not np.nan:
            data = pd.DataFrame(data['result']['data'])
            data = data.rename(columns=dict(zip(data.columns, data.columns.map(lambda x: x.lower()))))
            result = result.append(data, ignore_index=True)
    return result

if __name__ == "__main__":
    print(institution_holding('2022-03-03'))
