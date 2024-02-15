#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/12/11 10:47
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : Ip138.py
# @Software: PyCharm

from config import ip138wb
from tools.commons import readdomain
import requests
from bs4 import BeautifulSoup


def Ip138search(file,alldomain):
    domains = readdomain(file)
    ip138wb.append(['子域名'])
    for domain in domains:
        header={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        reald=domain.replace('\n','')
        url=f"https://chaziyu.com/{reald}/"
        try:
            r=requests.get(url,headers=header)
            soup = BeautifulSoup(r.text, "html.parser")

            trs=soup.find_all("table")[0].find_all('tbody')[0].find_all('tr')
            replace=[]

            for tr in trs:
                tds=tr.find_all('td')
                if tds[0].text not in replace:
                    print(tds[1].text)
                    alldomain.append(tds[1].text)
                    replace.append(tds[1].text)
                    ip138wb.append(tds[1].text)
        except:
            continue

