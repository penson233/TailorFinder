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
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tools import WebfingerScan,colorprint,systemcmd
from multiprocessing.pool import ThreadPool
import openpyxl
import ipaddress
from bs4 import BeautifulSoup
from config import masscan,nmap,webport
from tools import CheckCDN


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





def Port_Scan(outpath,name,portfile,onlyhttp,iscdn,onlyhttpThread):
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

    request=[]
    tbody=[]
    count=0

    with open(outpath+"/alive_ip.txt",'a+') as f:
        cdnlist={}

        for domain in columns[0]:
            result=systemcmd.subpross("dig +short "+domain.value)
            if result !=None:
                try:
                    res=result.split('\n')
                    for j in res:
                        if j !="":
                            if check_ip_type(j)== 4 or check_ip_type(j)== 6:
                                if domain.value not in iplist:
                                    if not is_internal_ip(j):
                                        iplist[domain.value] = [j]
                                        if iscdn:
                                            if CheckCDN.checkAll(outpath,domain.value):
                                                if domain.value not in cdnlist:
                                                    cdnlist[domain.value] = [j]
                                                    print("cdn :  ", domain.value, cdnlist[domain.value])
                                            else:
                                                if j not in read:
                                                    count+=1
                                                    print(j + "  :  " + domain.value)
                                                    f.write(j + '\n')
                                        else:
                                            if j not in read:
                                                count += 1

                                                iplist[domain.value].append(j)
                                                print(j + "  :  " + domain.value)

                                                f.write(j + '\n')


                                    else:
                                        print("内网: "+domain.value+" "+j)
                                        tbody.append({j: {'ip': domain.value, 'port': '', 'server': '', 'title':'内网ip', 'code': '', 'finger': ''}})
                                else:
                                    iplist[domain.value].append(j)

                except Exception as e:
                    print(e)


    print(iplist)

    with open(outpath+"/cdn.txt",'w') as f:
        f.write(str(cdnlist))


    with open("./finger/finger.json",'r') as f:
        fingerjson=json.loads(f.read())["fingerprint"]



    if onlyhttp == True:

        pool = ThreadPool(onlyhttpThread)

        for key in iplist:
            for port in webport:
                pool.apply_async(http_https_probe, args=(key + ":" + str(port), request, key, tbody, fingerjson,))
        pool.close()
        pool.join()



    else:
        systemcmd.runshell(masscan.format(outpath, outpath), "massscan")

        with open(outpath + "/alive_port.json", 'r') as f:
            read = json.loads(f.read().replace("{finished: 1}", ""))

        ip_port = {}
        for i in read:
            if i['ip'] not in ip_port:
                for j in i['ports']:
                    ip_port[i['ip']] = [str(j['port'])]
            else:
                for j in i['ports']:
                    ip_port[i['ip']].append(str(j['port']))

        if not os.path.exists(outpath + "/nmap"):
            os.mkdir(outpath + "/nmap")

        # nmap 扫描
        temp=[]
        temp2=[]
        for key in iplist:
            for ip in iplist[key]:
                #筛选masscan扫描的ip是否在域名解析里
                if ip in ip_port:
                    if key not in temp2:
                        temp2.append(key)
                    temp.append(ip)
                    systemcmd.runshell(
                        f"nmap {nmap} -p {','.join(ip_port[ip])} {key} -oX {outpath + '/nmap'}/nmap_{key}.xml",
                        "nmap")

                    systemcmd.runshell(
                        f"xsltproc -o {outpath + '/nmap'}/nmap_{key}.html ./bin/nmap/mode.xsl {outpath + '/nmap'}/nmap_{key}.xml",
                        "nmap")
                    #http探测
                    for port in ip_port[ip]:
                        http_https_probe(key + ":" + port, request, ip, tbody, fingerjson)

        #扫描masscan里没在域名解析里
        for ip_2 in ip_port:
            if ip_2 not in temp:
                systemcmd.runshell(
                    f"nmap {nmap} -p {','.join(ip_port[ip_2])} {ip_2} -oX {outpath + '/nmap'}/nmap_{ip_2}.xml",
                    "nmap")

                systemcmd.runshell(
                    f"xsltproc -o {outpath + '/nmap'}/nmap_{ip_2}.html ./bin/nmap/mode.xsl {outpath + '/nmap'}/nmap_{ip_2}.xml",
                    "nmap")
                # http探测
                for port in ip_port[ip_2]:
                    http_https_probe(iplist[ip_2] + ":" + port, request, ip_2, tbody, fingerjson)
        pool2 = ThreadPool(onlyhttpThread)

        #批量探测masscan没扫出来的东西
        for key in iplist:
            if key not in temp2:
                for ip_3 in iplist[key]:
                    for port in webport:

                        http_https_probe(key + ":" + str(port), request, ip_3, tbody, fingerjson)

        # 处理nmap扫描结果
        HandleNmap(outpath, name)

    with open(outpath+"/requests.txt",'w') as f:
        f.write('\n'.join(request))

    with open("tools/html/web.html",'r') as f:
        read=f.read()

    output=read.replace("penson",name+"收集结果").replace("var jsonData1 =;",f"var jsonData ={tbody}\n").replace('Portdetail.html',name+'_Portdetail.html')

    with open(outpath+"/"+name+"_web.html","w") as f:
        f.write(output)


    colorprint.Green("[+] success !!! saved in "+outpath)



def HandleNmap(outpath,filename):
    files=os.listdir(f"{outpath}/nmap")
    tbody = []
    for file in files:
        if "html" in file:
            with open(f"{outpath}/nmap/"+file) as f:
                read=f.read()
            domain="None"
            name=file.replace("nmap_","").replace(".html","")
            if not re.match("\d+\.\d+\.\d+\.\d+", name):
                domain=name

            HandleNmapHtml(domain,read,tbody)


    with open("tools/html/Portdetail.html",'r') as f:
        read= f.read()

    output=read.replace("penson", "端口收集结果").replace("var jsonData1 =;", f"var jsonData ={tbody}\n").replace('web.html',filename+"_web.html")
    with open(f"{outpath}/"+filename+"_Portdetail.html","w") as f:
        f.write(output)

def HandleNmapHtml(domain,read,tbody):
    soup = BeautifulSoup(read, 'html.parser')
    table_div =soup.find('table', id='table-services')

    body=table_div.find("tbody")
    rows = body.find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        row_data = [column.text.strip() for column in columns]
        tbody.append({domain:{'ip':row_data[0],'port':row_data[1],'protocol':row_data[2],'server':row_data[3],'zujian':row_data[4],'version':row_data[5],'cpe':row_data[6],'fu':row_data[7]}})

    return tbody



def http_https_probe(target,request,ip,tbody,fingerjson):
    # 拼接HTTP和HTTPS的URL
    http_url = f'http://{target}'
    https_url = f'https://{target}'


    temp=target.split(':')

    #发送http请求
    try:
        fingerlist = []
        httprequets(http_url, fingerjson, fingerlist, request, tbody, temp,ip)
    except requests.RequestException as e:
        pass

    #发送https请求
    try:
        fingerlist = []
        httprequets(https_url, fingerjson, fingerlist, request, tbody, temp,ip)
    except requests.RequestException as e:
        pass

def remove_invisible_chars(text):
    # 定义不可见字符的正则表达式模式
    invisible_chars_pattern = r'[\r\n\t ]'
    # 使用正则表达式替换不可见字符为空字符串
    cleaned_text = re.sub(invisible_chars_pattern, '', text)
    return cleaned_text

def httprequets(http_url,fingerjson,fingerlist,request,tbody,temp,ip):
    # 发送HTTP请求
    response_http = requests.get(http_url, timeout=2, verify=False, allow_redirects=False)
    request.append(http_url)
    try:
        context_type = response_http.headers["Content-Type"]
    except:
        context_type = ""
    try:
        resp_text = WebfingerScan.to_utf8(response_http.content.decode(), context_type)
    except:
        resp_text = WebfingerScan.to_utf8(response_http.text, context_type)

    error_code =[403,400,422]
    if response_http.status_code not in error_code:
        fingerlist = WebfingerScan.Scan(http_url, response_http, fingerjson,context_type)


    soup = BeautifulSoup(resp_text, 'html.parser')

    try:
        title = remove_invisible_chars(soup.find('title').text)

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
    else:
        fingers += "空,"

    tbody.append({temp[0]: {'ip': ip, 'port': temp[1], 'server': http_url, 'title': title,
                            'code': str(response_http.status_code), "finger": fingers[:-1]}})


def httpsrequest(https_url, fingerjson, fingerlist, request, tbody, temp,ip):
    # 发送HTTPS请求
        response_https = requests.get(https_url, timeout=2,verify=False, allow_redirects=False)
        request.append(https_url)
        try:
            context_type = response_https.headers["Content-Type"]
        except:
            context_type = ""
        try:
            resp_text = WebfingerScan.to_utf8(response_https.content.decode(), context_type)
        except:
            resp_text = WebfingerScan.to_utf8(response_https.text, context_type)

        if response_https.status_code != 403 and response_https.status_code != 400:
            fingerlist=WebfingerScan.Scan(https_url,resp_text,fingerjson,context_type)

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