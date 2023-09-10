import urllib.parse
import requests
import json
import time
from config import emailwb,veryvpcookie
from tools import colorprint
import sys

def veryvpfind(domain,allemail):


    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie': veryvpcookie,
        'Referer': 'http://veryvp.com'
    }

    while True:
        url_1 = "http://www.veryvp.com/SearchEmail/CreateSearch"

        r = requests.post(url_1, data={'domain': domain}, headers=header)
   
        if "任务已提交" in r.text:
            break
        if "请先登录" in r.text:
            colorprint.Red("[-]请到http://veryvp.com/获取登录cookie再尝试！！！")
            sys.exit(0)

    time.sleep(2)
    url_2 = "http://www.veryvp.com/SearchEmail/GetEmailList"
    r = requests.post(url_2, data={'Key': domain, 'PageSize': '10000', 'PageNo': '1', 'Order': ''}, headers=header)
    result = json.loads(urllib.parse.unquote(r.json()).replace("\"[", '[').replace(']\"', ']'))['Data']
    colorprint.Green("[+] " + domain + " find " + str(len(result)) + " emails on veryvp")
    for i in result:
        if i["email"] not in allemail:
            emailwb.append([i['email'],"veryvp"])
            allemail.append(i['email'])



