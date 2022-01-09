# ===
import requests

login_headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Cookie": "route=6562e3902d5c92ecb8a0200078ee0128; JSESSIONID=pG-1gONY4e06cf2tgPFcJXnKichLoGLPSa22deMQmgM8DS-iww1T!550765829; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN",
    "Referer": "https://ehall.nju.edu.cn/ywtb-portal/official/index.html"
}
post_data = {
    "username":	"MF20150026",
    "password":	"OOH6UXiDxRhYVcrnwgHYA69LC+8sCkMATiwCp8ko4M82m1N8QgLw0iGizVnS3U05t00cLWNn9Da3Nx9HsRuhwUE7YMMfhG5gf/wlBAw9JQo=",
    "lt":	"LT-5964656-Wr1QZoMx3AW7A2Y2vsZafHaxNwBN9X1622247822685-VivT-cas",
    "dllt":	"userNamePasswordLogin",
    "execution":	"e2s1",
    "_eventId":	"submit",
    "rmShown":	"1"
}

# %%
login_url = "https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fehall.nju.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nju.edu.cn%2Fywtb-portal%2Fofficial%2Findex.html"
login_res = requests.post(login_url, data=post_data, headers=login_headers, allow_redirects=False)
print(login_res.text)
