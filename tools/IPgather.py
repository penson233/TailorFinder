import openpyxl
import re
from collections import Counter
from tools import colorprint
import os

def readxls(outpath,name,allip):
    colorprint.Red("[-]start to gather ip....")
    workbook = openpyxl.load_workbook(outpath+"/test.xlsx")

    workbook.create_sheet("fofa_ip", 12)
    workbook.create_sheet("hunter_ip", 13)
    workbook.create_sheet("allip",14)

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








    '''存储'''
    allip_sheet = workbook["allip"]
    all_ip= Counter(allip).most_common()


    allip_sheet.append(["c段","次数"])


    for all in all_ip:
        all_ips=find_c.findall(all[0])
        allip_sheet.append([all_ips[0]+ ".0/24",all[1]])


    fofa_ip = workbook["fofa_ip"]
    fofa_ip.append(['c段', '次数'])

    for all in fofa_all:
        fofa_ip.append([all[0] + ".0/24", all[1]])

    hunter_ip = workbook["hunter_ip"]
    hunter_ip.append(["c段", "次数"])

    for all in hunter_all:

        hunter_ip.append([all[0] + ".0/24", all[1]])




    workbook.save(outpath+"/"+name+".xlsx")
    os.system("rm -f "+outpath+"/test.xlsx")