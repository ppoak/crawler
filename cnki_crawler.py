import requests

url = "https://kns.cnki.net/KNS8/Brief/GetGridTableHtml"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "kns.cnki.net",
    "Origin": "https://kns.cnki.net",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Connection": "keep-alive",
    "Referer": "https://kns.cnki.net/kns8/defaultresult/index",
    "Content-Length": "948",
    "Cookie": r"_pk_id=d45e0759-9a57-4d99-873e-238345154f5e.1632660741.11.1633176590.1633173780.; _pk_ses=*; CurrSortField=%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27); CurrSortFieldType=desc; dSearchFold=undefined; dperpage=20; dsorder=pubdate; dstyle=listmode; dversion=undefined; knsLeftGroupSelectItem=; language=undefined; searchTimeFlag=0; showlist=CJFQ%2CCDMD%2CCIPD%2CCCND%2CBDZK%2CCISD%2CSNAD%2CCCJD%2CGXDB_SECTION%2CCJFN%2CCCVD%2CCLKLK%2C1633176385537; Ecp_loginuserbk=sh0301; Ecp_session=1; SID_kns=025123114; SID_klogin=125141; SID_kvisual=125105; Ecp_ClientId=6210601193101184315; SID_krsnew=125134; SID_kxreader_new=011121; yeswholedownload=%3Bhbjr202109013; SID_kcms=124115; Ecp_IpLoginFail=21092949.77.147.157; Ecp_ClientIp=49.77.147.157; SID_kns_new=kns123110; ASP.NET_SessionId=gvufzaeqj1tfkdqfvhgn4lo3; SID_kns8=123122; UM_distinctid=17c24ac48c57d5-06bb1faa9fadd5-3e62684b-13c680-17c24ac48c6e28; cnkiUserKey=49e5aa07-7a8f-6bc6-74a6-f11a20f039c8",
    "X-Requested-With": "XMLHttpRequest"
}
data = {
    "IsSearch": 'true',
    "QueryJson": '{"Platform":"","DBCode":"SCDB","KuaKuCode":"CJFQ,CDMD,CIPD,CCND,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD,CLKLK","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":1,"Items":[{"Title":"主题","Name":"SU","Value":"反洗钱","Operate":"%=","BlurType":""}],"ChildItems":[]}]}}',
    "PageName": 'DefaultResult',
    "DBCode": 'SCDB',
    "KuaKuCodes": 'CJFQ,CDMD,CIPD,CCND,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD,CLKLK',
    "CurPage": '1',
    "RecordsCntPerPage": '20',
    "CurDisplayMode": 'listmode',
    "CurrSortField": r'%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27)',
    "CurrSortFieldType": 'desc',
    "IsSentenceSearch": 'false',
    "Subject": '',
}

res = requests.post(url, data=data, headers=headers)
print(res.status_code)
print(res.text)