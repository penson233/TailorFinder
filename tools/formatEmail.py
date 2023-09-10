#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 11:45
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : formatEmail.py
# @Software: PyCharm
import requests
from config import emailwb
from tools import colorprint
from bs4 import BeautifulSoup

def formatemailFind(domain,allemail):
    url=f"https://www.email-format.com/d/{domain}/"
    header = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
    }
    try:
        r=requests.get(url=url,headers=header,timeout=5)
        if "/i/main/" not in r.url:
            soup=BeautifulSoup(r.text, "html.parser")
            trs = soup.find_all("table")[0].find_all('tbody')[0].find_all('tr')
            colorprint.Green("[+] " + domain + " find " + str(len(trs)) + " emails on email-format")
            for tr in trs:
                tds = tr.find_all('td')
                email=tds[0].find(class_='fl').text.replace('\n','').replace(' ','')
                if email not in allemail:
                    emailwb.append([email,"email-format"])
                    allemail.append(email)
        else:
            colorprint.Green("[+] " + domain + " find 0 "+" emails on email-format")
    except Exception as e:
        print("email-format: "+str(e))