#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 22:56
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : tyc.py
# @Software: PyCharm
import time

import requests
import re
import json
from config import tyccookie,tyctoken
from tools import colorprint


def finddomain(companyId,result):

    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    'Cookie': tyccookie
            }

    url_2="https://capi.tianyancha.com/cloud-intellectual-property/intellectualProperty/icpRecordList?id="+str(companyId)+"&pageSize=10&pageNum=1"
    r=requests.get(url_2,headers=header)

    time.sleep(2)

    results=json.loads(r.text)['data']

    if results["itemTotal"] !=0:
        for i in results["item"]:

            result.append([i["companyName"],'',i['ym'], i['liscense'],'天眼查'])


def findalldomain(name,percent,count):

    result=[]
    idre=re.compile("type=\"application/json\">(.*?)</script>")

    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Cookie':tyccookie
            }

    #找到公司id
    url_1="https://www.tianyancha.com/search"
    r=requests.get(url_1+"?key="+name,headers=header)

    idresult=json.loads(idre.findall(r.text)[0])['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyList']

    companyId=idresult[0]['id']

    #找到公司根域名
    finddomain(companyId,result)

    #找到子公司
    childrens=findchildren(companyId)

    findchildrens=[]
    for j in childrens:
        try:
            if int(float(j[3].replace('%',''))) >= percent:
                finddomain(j[2],result)
                findchildrens.append(j)
        except Exception as e:
            if j[3]=='-':
                print("不知控股比例: "+j[0])
            else:
                print(e)


    #找到分支机构
    fenzhi_id=findfenzhijigou(companyId,count)
    if len(fenzhi_id)> 0:
        for fenzhi in fenzhi_id:

            finddomain(fenzhi,result)


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


#查找分支机构
def findfenzhijigou(id,count):
    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Cookie':tyccookie,
        'X-Auth-Token': tyctoken,
        'Version': 'TYC-Web',
        'Origin': 'https://www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
            }
    fenzhi_company_id = []

    for i in range(10,count):

        url="https://capi.tianyancha.com/cloud-company-background/company/branchList?gid={}&pageSize={}&pageNum=1".format(id,i//10)
        r = requests.get(url, headers=header)
        if "result" in json.loads(r.text)['data']:
            results = json.loads(r.text)['data']['result']

            for i in results:
                if i not in fenzhi_company_id:
                    fenzhi_company_id.append(i['id'])

        elif "total" in json.loads(r.text)['data']:
            colorprint.Green(f"[+] tian_yan_cha found find {json.loads(r.text)['data']['total']} branch")
            break

        i+10

    else:
        colorprint.Green(f"[+] tian_yan_cha found  not find branch")

    return fenzhi_company_id