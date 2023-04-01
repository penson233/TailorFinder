import openpyxl
import re
from collections import Counter
from tools import colorprint
import os
import aiodns
import asyncio
import sys

if sys.platform=="win32" or sys.platform=="win64":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
async def query(name, query_type):
    return await resolver.query(name, query_type)

def readxls(outpath,name):
    colorprint.Red("[-]start to gather ip....")
    workbook = openpyxl.load_workbook(outpath+"/test.xlsx")

    workbook.create_sheet("fofa_ip", 13)
    workbook.create_sheet("hunter_ip", 14)
    workbook.create_sheet("all_ip",15)

    fofa_iplist = []
    hunter_iplist = []
    ip_fan_fofa = []
    ip_fan_hunter = []

    '''获取fofa收集到的ip'''
    fofa = workbook["fofa"]
    find_c = re.compile("(\d+\.\d+\.\d+)\.")

    columns = list(fofa.columns)

    for i in columns[2]:
        if i.value != "ip":
            if i.value not in ip_fan_fofa:
                try:
                    c = find_c.findall(i.value)[0]
                    fofa_iplist.append(c)
                    ip_fan_fofa.append(i.value)
                except:
                    continue

    fofa_all = Counter(fofa_iplist).most_common()

    '''获取hunter收集到的ip'''
    hunter = workbook["hunter"]
    columns = list(hunter.columns)
    for i in columns[1]:
        if i.value != "ip":
            if i.value not in ip_fan_hunter:
                try:
                    c = find_c.findall(i.value)[0]
                    hunter_iplist.append(c)
                    ip_fan_hunter.append(i.value)
                except:
                    continue

    hunter_all = Counter(hunter_iplist).most_common()





    fofa_ip = workbook["fofa_ip"]
    fofa_ip.append(['c段', '次数'])

    for all in fofa_all:
        fofa_ip.append([all[0] + ".0/24", all[1]])

    hunter_ip = workbook["hunter_ip"]
    hunter_ip.append(["c段", "次数"])

    for all in hunter_all:
        hunter_ip.append([all[0] + ".0/24", all[1]])





    #收集c段，并通过对比A段判断是否是泛解析
    all_ip_repeat=[]

    all_domain_wb=workbook["alldomain"]
    columns = list(all_domain_wb.columns)

    all_ip_wb=workbook["all_ip"]
    all_ip_wb.append(['c段','次数','去掉泛解析域名'])

    real_domain=[]

    ipreg = re.compile("\d+\.\d+\.\d+\.\d+")

    ip_domain={}
    with open(outpath + "error_domain.txt", 'w') as f:
        for all in columns[0]:
            if all.value !="alldomain":
                try:
                    coro = query(all.value, 'A')
                    result = loop.run_until_complete(coro)
                    ipfind = ipreg.findall(str(result[0]))[0]

                    if ipfind not in ip_domain:
                        ip_domain[ipfind] = [all.value]
                        ip_find=find_c.findall(ipfind)[0]
                        all_ip_repeat.append(ip_find)
                        real_domain.append(all.value)
                    else:
                        ip_domain[ipfind].append(all.value)
                except:

                        print("error domain:  "+all.value)
                        f.write(all.value+'\n')
                        continue





    all_ip_conut= Counter(all_ip_repeat).most_common()
    print(all_ip_conut)
    real_wb=[]
    for all_ip in all_ip_conut:
        real_wb.append([all_ip[0] + ".0/24", all_ip[1]])
    with open(outpath+'/realdomain.txt','w') as f:
        for i in range(len(real_domain)):
            if i < len(real_wb):
                real_wb[i].append(real_domain[i])
            else:
                real_wb.append(["","",real_domain[i]])
            f.write(real_domain[i]+'\n')

    for j in real_wb:
        all_ip_wb.append(j)







    workbook.save(outpath+"/"+name+".xlsx")
    os.system("rm -f "+outpath+"/test.xlsx")