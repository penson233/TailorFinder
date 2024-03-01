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
import time
import math
import requests
from config import aqccookie
from tools import colorprint


def finddomain(pid,result,name,type=0,percent=0):
    url="https://aiqicha.baidu.com/detail/intellectualPropertyAjax?pid="+str(pid)
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Zx-Open-Url': 'https://aiqicha.baidu.com/company_detail_'+str(pid),
        'Referer': 'https://aiqicha.baidu.com/company_detail_'+str(pid)
    }
    r=requests.get(url,headers=header)
    resultj=json.loads(r.text)['data']['icpinfo']

    for i in resultj['list']:
        if type==1:
            result.append([name,i['siteName'],'\n'.join(i['domain']),i['icpNo'],'爱企查','是','0'])
        elif percent!=0:
            result.append([name, i['siteName'], '\n'.join(i['domain']), i['icpNo'], '爱企查', '是', str(percent)+"%"])
        else:
            result.append([name, i['siteName'], '\n'.join(i['domain']), i['icpNo'], '爱企查', '否', '0'])

def findalldomain(name,percent):

    result=[]
    appresult = []
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers'
    }



    url_1="https://aiqicha.baidu.com/s?q="+name+"&t=0"
    # 找子公司
    findchildrens = []
    r=requests.get(url=url_1,headers=header)

    findre=re.compile("window.pageData = (.*?\});")

    if len(json.loads(findre.findall(r.text)[0])['result']['resultList']) > 0:
        companyId=json.loads(findre.findall(r.text)[0])['result']['resultList'][0]['pid']
        companyname=json.loads(findre.findall(r.text)[0])['result']['resultList'][0]['titleName']

        finddomain(companyId,result,companyname)
        time.sleep(2)
        findapp(companyId,name,appresult)



        childrens=findchildren(companyId)



        for children in childrens:
            try:
                if int(float(children[2].replace('%',''))) >= percent:
                    time.sleep(1)
                    finddomain(children[1],result,children[0],percent=int(float(children[2].replace('%',''))))
                    time.sleep(1)
                    findapp(children[1],children[0],appresult)
                    time.sleep(1)
                    findchildrens.append(children)
            except:
                if children[2]=='-':
                    print("不知名控股比例: "+children[0])

        #找分支机构
        fenzhi_id=findbranch(companyId)

        for j in fenzhi_id:
            finddomain(j[1],result,j[0],type=1)
            time.sleep(2)
        colorprint.Green("[+] ai_qi_cha found "+str(len(fenzhi_id))+" branch")


        colorprint.Green("[+]ai_qi_cha found " + str(len(findchildrens)) + " invested company "+"and "+str(len(appresult))+" apps")
    else:
        colorprint.Red("[-]ai_qi_cha not found!!!")
    return result,findchildrens,appresult

def findchildren(pid):
    results=[]
    header={
        'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie':aqccookie,
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Zx-Open-Url': 'https://aiqicha.baidu.com/company_detail_'+str(pid),
        'Referer': 'https://aiqicha.baidu.com/company_detail_'+str(pid)
    }

    time.sleep(1)

    url="https://aiqicha.baidu.com/stockchart/stockchartAjax?pid="+str(pid)+"&drill=0"
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
        'Zx-Open-Url': 'https://aiqicha.baidu.com/company_detail_'+str(pid),
        'Referer': 'https://aiqicha.baidu.com/company_detail_'+str(pid)
    }

    url="https://aiqicha.baidu.com/detail/compManageAjax?pid="+str(pid)
    r = requests.get(url, headers=header)
    resultj = json.loads(r.text)['data']['appinfo']['list']
    if len(resultj)>0:
        for i in resultj:

            results.append([i['name'], i['classify'], i['logoBrief'],name])

    return results

#找分支机构
def findbranch(id):


    url="https://aiqicha.baidu.com/detail/branchajax?p=1&size=10&pid={}".format(id)
    header = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Cookie': aqccookie,
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Zx-Open-Url': "https://aiqicha.baidu.com/company_detail_{}".format(id),
        'Referer': "https://aiqicha.baidu.com/company_detail_{}".format(id)
    }

    r=requests.get(url,headers=header).json()
    fenzhi_id=[]



    if len(r['data']['list']) >0:
        for i in r['data']['list']:
            if i not in fenzhi_id:
                fenzhi_id.append([i['entName'],i['pid']])

        allpage = math.ceil(r['data']['totalNum'] // 10)
        for num in range(2, allpage+1):
            url = "https://aiqicha.baidu.com/detail/branchajax?p={}&size=10&pid={}".format(num,id)
            r = requests.get(url, headers=header).json()
            for i in r['data']['list']:
                if i not in fenzhi_id:
                    fenzhi_id.append([i['entName'], i['pid']])



    return fenzhi_id



