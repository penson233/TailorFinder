#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 22:56
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : tyc.py
# @Software: PyCharm
import requests
import re
import json
from config import tyccookie
from tools import colorprint


def finddomain(companyId,result):

    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    'Cookie': tyccookie
            }

    url_2="https://capi.tianyancha.com/cloud-intellectual-property/intellectualProperty/icpRecordList?id="+str(companyId)+"&pageSize=10&pageNum=1"
    r=requests.get(url_2,headers=header)
    results=json.loads(r.text)['data']
    if results["itemTotal"] !=0:
        for i in results["item"]:
            result.append([i["companyName"],i['ym'], i['liscense'],'天眼查'])

def findalldomain(name,percent):

    result=[]
    idre=re.compile("type=\"application/json\">(.*?)</script>")

    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Cookie':tyccookie
            }


    url_1="https://www.tianyancha.com/search"
    r=requests.get(url_1+"?key="+name,headers=header)
    idresult=json.loads(idre.findall(r.text)[0])['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyList']

    companyId=idresult[0]['id']


    finddomain(companyId,result)

    childrens=findchildren(companyId)

    findchildrens=[]
    for j in childrens:
        if int(float(j[3].replace('%',''))) >= percent:
            finddomain(j[2],result)
            findchildrens.append(j)


    colorprint.Green("[+]tian_yan_cha found "+str(len(findchildrens))+" invested company")
    return result,findchildrens



def findchildren(id):
    result=[]

    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Cookie':tyccookie
            }

    url="https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id="+str(id)
    r=requests.get(url,headers=header)
    results=json.loads(r.text)['data']['investorList']
    for i in results:
        result.append([i['name'],i['amount'],i['id'],i['percent']])

    return result

