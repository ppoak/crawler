import requests
from bs4 import BeautifulSoup
import os
import json
import execjs

def cas_login(username, password):
    """
    校园网MOD-CAS登录机制
    ===================
    username: str -> 用户名
    password: str -> 密码
    ===================
    return: str -> 登录使用的cookie
    """

    # 1. 初次访问autherserver网站
    auth_url = r"https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fehall.nju.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nju.edu.cn%2Fywtb-portal%2Fofficial%2Findex.html"
    auth_headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
    }
    auth_res = requests.get(auth_url, headers=auth_headers)

    # 解析html，获取cookies
    auth_soup = BeautifulSoup(auth_res.text, 'lxml')
    login_form = auth_soup.select_one("#casLoginForm")
    salt = login_form.select_one("#pwdDefaultEncryptSalt")["value"]
    rmShown = login_form.select_one("input[name='rmShown']")["value"]
    eventId = login_form.select_one("input[name='_eventId']")["value"]
    execution = login_form.select_one("input[name='execution']")["value"]
    dllt = login_form.select_one("input[name='dllt']")["value"]
    lt = login_form.select_one("input[name='lt']")["value"]
    # password = login_form.select_one("input[name='password']")["value"]
    cookie = requests.utils.dict_from_cookiejar(auth_res.cookies)
    cookie_str = ""
    for k, v in cookie.items():
        cookie_str += k + "=" + v + "; "

    # 将salt传入lib/encrypt.js并获取加密后的密码
    with open("./lib/encrypt.js", 'r') as f:
        encrypt_code = f.read()
    encrypt_code_compiled = execjs.compile(encrypt_code)
    password_encrypted = encrypt_code_compiled.call('encryptAES', password, salt)

    #  构造登录请求头以及post数据
    login_headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
        "Cookie": cookie_str,
        "Referer": "https://ehall.nju.edu.cn/ywtb-portal/official/index.html"
    }
    post_data = {
        "username":	username, # 要求输入
        "password":	password_encrypted,
        "lt": lt,
        "dllt":	dllt,
        "execution": execution,
        "_eventId":	eventId,
        "rmShown":	rmShown
    }

    # 开发使用，如果需要则在login_res中加入proxies=proxies
    # proxies = {
    #     "http": "http://175.44.109.179:9999"
    # }

    # 2. 构造登录请求
    login_url = "https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fehall.nju.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nju.edu.cn%2Fywtb-portal%2Fofficial%2Findex.html"
    login_res = requests.post(login_url, data=post_data, headers=login_headers, allow_redirects=False)

    # 3. 提取ticket
    login_soup = BeautifulSoup(login_res.text, 'lxml')
    redirect_url = login_soup.select_one("p a")["href"]

    # 4. 跳转到redirect_url
    session = requests.session()
    session.get(redirect_url, headers=login_headers, allow_redirects=False)

    #  5. 解析cookie
    login_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    login_cookie_str = ""
    for k, v in login_cookie.items():
        login_cookie_str += k + '=' + v + '; '
    
    return login_cookie_str + cookie_str


def beat_card(cookie, place):
    """
    打卡函数
    =======
    cookie: str -> 登录信息
    place: str -> 打卡地点
    =======
    return: tuple -> (打卡是否成功, 打卡信息)
    """

    place_dict = {
        "liangjiang": "江苏省南京鼓楼区两江路",
        "qinshi1": "江苏省南京市鼓楼区汉口路27-1号",
        "qinshi2": "江苏省南京市鼓楼区汉口路27-2号",
        "jiaoshi": "江苏省南京市鼓楼区天津路"
    }
    if place in place_dict:
        place = place_dict[place]
        
    # 请求参数设定
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Cookie": cookie
    }
    getinfo_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do"

    # 打卡信息获取
    info = requests.get(getinfo_url, headers=headers)
    wid = json.loads(info.text)["data"][0]["WID"]

    # 打卡url设定及打卡
    daka_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do?WID=" + wid + \
            "&CURR_LOCATION=" + place + "&IS_TWZC=1&IS_HAS_JKQK=1&JRSKMYS=1&JZRJRSKMYS=1"
    daka = requests.get(daka_url, headers=headers)

    # 处理打卡结果
    daka_status = json.loads(daka.text)["msg"]

    if daka_status == "成功":
        return True, daka_status  
    else:
        return False, daka_status  

if __name__ == "__main__":

    # 切换工作目录
    current_path = os.path.split(os.path.abspath(__file__))[0]
    os.chdir(current_path)
    # 登录
    cookie = cas_login("", "")
    # 打卡
    success, msg = beat_card(cookie, "qinshi2")
    print("打卡状态: " + msg)
