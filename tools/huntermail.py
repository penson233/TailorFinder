#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 10:56
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : huntermail.py
# @Software: PyCharm
import requests
from config import emailwb,hunteremailkey
from tools import colorprint


def hunterfindemail(domain,allemail):
    url=f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={hunteremailkey}"

    header={
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        "Content-Type": "application/json"
    }

    try:
        r=requests.get(url=url,headers=header,timeout=5).json()['data']
        emails=r['emails']
        colorprint.Green("[+] " + domain + " find " + str(len(emails)) + " emails on hunter.io")
        for email in emails:
            if email['value'] not in allemail:
                emailwb.append([email['value'],"hunter.io"])
                allemail.append(email['value'])
    except Exception as e:
        print("hunter.io "+str(e))


