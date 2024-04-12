#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 17:25
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : Portscan.py
# @Software: PyCharm
import json
import os
import re
import requests
from tools.commons import pre_html,aft_html
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tools import WebfingerScan,colorprint,systemcmd
import openpyxl
import ipaddress
from bs4 import BeautifulSoup
from config import masscan,nmap

# 禁用警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def is_internal_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        # Invalid IP address format
        return False

def check_ip_type(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        if ip.version == 4:
            return 4
        elif  ip.version == 6:
            return 6
        else:
            return 0
    except ValueError:
        return False


def Port_Scan(outpath,name,portfile):
    colorprint.Red("[-]start to scaning ip....")
    if portfile!="":
        workbook = openpyxl.load_workbook(portfile)
    else:
        workbook = openpyxl.load_workbook(outpath+"/"+name+".xlsx")

    alive_ip=workbook["alive_domain"]

    columns = list(alive_ip.columns)
    iplist={}
    with open(outpath+"/alive_ip.txt") as f:
        read=f.read().split('\n')[:-1]


    with open(outpath+"/alive_ip.txt",'a+') as f:
        for domain in columns[0]:

            result=systemcmd.subpross("dig +short "+domain.value)
            if result !="":
                try:
                    res=result.split('\n')
                    for j in res:
                        if j !="":
                            if check_ip_type(j)== 4 or check_ip_type(j)== 6:
                                if j not in iplist:
                                    if check_ip_type(j)== 4 or check_ip_type(j)== 6:
                                        if not is_internal_ip(j):
                                            iplist[j] = domain.value
                                            print(j+"  :  "+domain.value)
                                            if j not in read:
                                                f.write(j+'\n')
                                        else:
                                            print("内网: "+domain.value+" "+j)
                except Exception as e:
                    print(e)


    print(iplist)



    systemcmd.runshell(masscan.format(outpath,outpath),"massscan")

    with open("./finger/finger.json",'r') as f:
        fingerjson=json.loads(f.read())["fingerprint"]

    with open(outpath+"/alive_port.json",'r') as f:
        read=json.loads(f.read().replace("{finished: 1}",""))


    ip_port={}
    for i in read:
        if i['ip'] not in ip_port:
            for j in i['ports']:
                ip_port[i['ip']]=[str(j['port'])]
        else:
            for j in i['ports']:
                ip_port[i['ip']].append(str(j['port']))


    if not os.path.exists(outpath+"/nmap"):
        os.mkdir(outpath+"/nmap")




    request=[]
    tbody=[]

    #nmap 扫描
    for key in ip_port:
        if key in iplist:
            systemcmd.runshell(f"nmap {nmap} -p {','.join(ip_port[key])} {key} -oX {outpath+'/nmap'}/nmap_{iplist[key]}.xml","nmap")

            systemcmd.runshell(f"xsltproc -o {outpath+'/nmap'}/nmap_{iplist[key]}.html ./bin/nmap/mode.xsl {outpath+'/nmap'}/nmap_{iplist[key]}.xml","nmap")

            for port in ip_port[key]:
                http_https_probe(iplist[key]+":"+port,request,key,tbody,fingerjson)
        else:
            systemcmd.runshell(
                f"nmap {nmap} -p {','.join(ip_port[key])} {key} -oX {outpath + '/nmap'}/nmap_{key}.xml",
                "nmap")

            systemcmd.runshell(
                f"xsltproc -o {outpath + '/nmap'}/nmap_{key}.html ./bin/nmap/mode.xsl {outpath + '/nmap'}/nmap_{key}.xml",
                "nmap")

            for port in ip_port[key]:
                http_https_probe(key + ":" + port, request, key, tbody,fingerjson)

    with open(outpath+"/requests.txt",'w') as f:
        f.write('\n'.join(request))

    with open(outpath+"/"+name+"_web.html","w") as f:
        f.write(pre_html.replace("penson",name+"收集结果")+f"var jsonData ={tbody}"+aft_html)


    #处理nmap扫描结果
    HandleNmap(outpath)
    colorprint.Green("[+] success !!! saved in "+outpath)


def HandleNmap(outpath):
    nmapcsv="域名,IP,端口,协议,服务,组件,版本,CPE,附加信息\n"
    files=os.listdir(f"{outpath}/nmap")
    for file in files:
        if "html" in file:
            with open(f"{outpath}/nmap/"+file) as f:
                read=f.read()
            domain="None"
            name=file.replace("nmap_","").replace(".html","")
            if not re.match("\d+\.\d+\.\d+\.\d+", name):
                domain=name

            nmapcsv+=HandleNmapHtml(domain,read)
    with open(f"{outpath}/Portdetail.csv","w") as f:
        f.write(nmapcsv)

def HandleNmapHtml(domain,read):
    soup = BeautifulSoup(read, 'html.parser')
    table_div =soup.find('table', id='table-services')

    body=table_div.find("tbody")
    rows = body.find_all('tr')

    temp=""
    for row in rows:
        columns = row.find_all('td')
        row_data = [column.text.strip() for column in columns]
        temp+=domain+","+','.join(row_data)+"\n"
    return temp



def http_https_probe(target,request,ip,tbody,fingerjson):
    # 拼接HTTP和HTTPS的URL
    http_url = f'http://{target}'
    https_url = f'https://{target}'

    temp=target.split(':')
    fingerlist=[]
    #发送http请求
    try:
        httprequets(http_url, fingerjson, fingerlist, request, tbody, temp,ip)
    except requests.RequestException as e:
        pass

    #发送https请求
    try:
        httprequets(https_url, fingerjson, fingerlist, request, tbody, temp,ip)
    except requests.RequestException as e:
        pass


def httprequets(http_url,fingerjson,fingerlist,request,tbody,temp,ip):
    # 发送HTTP请求
    response_http = requests.get(http_url, timeout=5, verify=False, allow_redirects=True)
    request.append(http_url)
    try:
        context_type = response_http.headers["Content-Type"]
    except:
        context_type = ""

    resp_text = WebfingerScan.to_utf8(response_http.content.decode(), context_type)

    error_code =[403,400,422]
    if response_http.status_code not in error_code:
        fingerlist = WebfingerScan.Scan(http_url, response_http, fingerjson,context_type)


    soup = BeautifulSoup(resp_text, 'html.parser')

    try:
        title = soup.find('title').text

        if title == "":
            title = "None"
    except:
        title = "None"
    fingers = ""
    if len(fingerlist) > 0:
        for finger in fingerlist:
            if "request" not in finger:
                fingers += finger["cms"] + ","
            else:
                fingers += f"[{finger['cms']},{finger['request']['path']}]" + " , "

    tbody.append({temp[0]: {'ip': ip, 'port': temp[1], 'server': http_url, 'title': title,
                            'code': str(response_http.status_code), "finger": fingers[:-1]}})


def httpsrequest(https_url, fingerjson, fingerlist, request, tbody, temp,ip):
    # 发送HTTPS请求
        response_https = requests.get(https_url, timeout=5,verify=False, allow_redirects=True)
        request.append(https_url)
        try:
            context_type = response_https.headers["Content-Type"]
        except:
            context_type = ""

        resp_text = WebfingerScan.to_utf8(response_https.content.decode(), context_type)

        if response_https.status_code != 403 and response_https.status_code != 400:
            fingerlist=WebfingerScan.Scan(https_url,resp_text,fingerjson)

        soup = BeautifulSoup(resp_text, 'html.parser')

        try:
            title = soup.find('title').text

            if title == "":
                title="None"
        except:
            title="None"

        fingers=""
        for finger in fingerlist:
            if "request" not in finger:
                fingers += finger["cms"] + ","
            else:
                fingers += f"[{finger['cms']},{finger['request']['path']}]" + " , "

        tbody.append({temp[0]:{'ip':ip,'port':temp[1],'server':https_url,'title':title, 'code':str(response_https.status_code),"finger":fingers[:-1]}})

