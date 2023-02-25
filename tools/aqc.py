#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 09:59
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : aqc.py
# @Software: PyCharm
import re
import json
import requests
from config import aqccookie
from tools import colorprint


def finddomain(pid,result):
    url="https://aiqicha.baidu.com/detail/intellectualPropertyAjax?pid="+str(pid)
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer':'https://aifanfan.baidu.com/'
    }
    r=requests.get(url,headers=header)
    resultj=json.loads(r.text)['data']['icpinfo']

    for i in resultj['list']:
        result.append([i['siteName'],'\n'.join(i['domain']),i['icpNo'],'爱企查'])

def findalldomain(name,percent):

    result=[]
    appresult = []
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer':'https://aifanfan.baidu.com/'
    }

    url_1="https://aiqicha.baidu.com/s?q="+name+"&t=0"

    r=requests.get(url=url_1,headers=header)
    findre=re.compile("window.pageData = (.*?\});")

    companyId=json.loads(findre.findall(r.text)[0])['result']['resultList'][0]['pid']

    finddomain(companyId,result)
    findapp(companyId,name,appresult)



    childrens=findchildren(companyId)



    findchildrens=[]
    for children in childrens:

        if int(float(children[2].replace('%',''))) >= percent:
            finddomain(children[1],result)
            findapp(children[1],children[0],appresult)
            findchildrens.append(children)



    colorprint.Green("[+]ai_qi_cha found " + str(len(findchildrens)) + " invested company")
    return result,findchildrens,appresult

def findchildren(pid):
    results=[]
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer':'https://aifanfan.baidu.com/'
    }

    url="https://aiqicha.baidu.com/detail/basicAllDataAjax?pid="+str(pid)
    r=requests.get(url,headers=header)
    resultj=json.loads(r.text)['data']['investRecordData']['list']

    for i in resultj:
        results.append([i['entName'],i['pid'],i['regRate'],i['regCapital']])

    return results


def findapp(pid,name,results):
    header = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie': aqccookie,
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://aifanfan.baidu.com/'
    }

    url="https://aiqicha.baidu.com/detail/compManageAjax?pid="+str(pid)
    r = requests.get(url, headers=header)
    resultj = json.loads(r.text)['data']['appinfo']['list']
    if len(resultj)>0:
        for i in resultj:
            results.append([i['name'], i['classify'], i['logoBrief'],name])

    return results