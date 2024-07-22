#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/4 10:41
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : CheckCDN.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
import dns.resolver
import requests
import ipaddress
import geoip2.database
import socket
import sys
import re
from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED


def matched(obj,list):
    #print(obj)
    for i in list:
        if i in obj:
            return True
    return False


def getCNAMES(domain):
    cnames = []
    cname = getCNAME(domain)
    if cname is not None:
        cnames.append(cname)
    while(cname != None):
        cname = getCNAME(cname)
        if cname is not None:
            cnames.append(cname)
    return cnames

def getCNAME(domain):
    try:
        answer = dns.resolver.resolve(domain,'CNAME')
    except:
        return None
    cname = [_.to_text() for _ in answer][0]
    return cname


def checkIP(ip):
    try:
        for cdn in cdns:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(cdn):
                return True
        return False
    except:
        return False

def getIP(domain):
    try:
        addr = socket.getaddrinfo(domain,None)
    except:
        return None
    return str(addr[0][4][0])


def checkASN(ip):
    try:
        with geoip2.database.Reader('./db/GeoLite2-ASN.mmdb') as reader:
            response = reader.asn(ip)
            for i in ASNS:
                if response.autonomous_system_number == int(i):
                    return True
    except:
        return False
    return False



def wFile(file,str):
    try:
        f = open(file,'a')
        f.write(str)
        f.write('\n')
    finally:
        f.close()

def checkAll(outpath,data):
    if not re.search(r'\d+\.\d+\.\d+\.\d+', data):
        ip = getIP(data)
    else:
        ip = data



    cdnip = checkIP(ip)

    if cdnip == True:
        print(data+": CDN")
        wFile(outpath+'/cdn.txt',data)
        return True

    cdnasn = checkASN(ip)
    if cdnasn == True:
        print(data+": CDN")
        wFile(outpath+'/cdn.txt',data)
        return True

    if not re.search(r'\d+\.\d+\.\d+\.\d+', data):
        cnames = getCNAMES(data)
        match = False
        for i in cnames:
            match = matched(i,all_CNAME)
            if match == True:
                break
        if match == True:
            print(data+": CDN")
            wFile(outpath+'/cdn.txt',data)
            return True

    wFile(outpath+'/host.txt',data)
    return False


