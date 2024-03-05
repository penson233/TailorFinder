#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/12/11 10:47
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : Ip138.py
# @Software: PyCharm

from config import ip138wb
from tools import colorprint
import requests
from bs4 import BeautifulSoup


def Ip138search(domain,alldomain):
    ip138wb.append(['子域名'])

    header={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    reald=domain.replace('\n','')
    url=f"https://chaziyu.com/{reald}/"
    try:
        r=requests.get(url,headers=header)
        soup = BeautifulSoup(r.text, "html.parser")
        table=soup.find_all("table")
        if len(table) >0:
            trs=table[0].find_all('tbody')[0].find_all('tr')
            if len(trs) > 0:
                colorprint.Green(f"\n[+] found {len(trs)} in {domain}")
                for tr in trs:
                    tds=tr.find_all('td')
                    if len(tds) > 0:
                        if "子域名" not in tds[1].text:
                            if tds[1].text not in alldomain:
                                 alldomain.append(tds[1].text)

                            ip138wb.append([tds[1].text])
        else:
            print(f"\n[-]no found in {domain}")
    except Exception as e:
        print(f"\n[-]no found in {domain}")

