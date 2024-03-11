#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 11:37
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : main.py
# @Software: PyCharm

import argparse
import os
import sys
from tools import colorprint,Portscan
import time
from functions import findallDomain,CollectSubdomain,CreateDatabase,HandleTable

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TailorFinder powered by penson\nA asset collection tool for Chinese enterprises\n such as\n\npython3 main.py -name 王尼玛有限公司 -p 100 -o ./test/')
    parser.add_argument('-name', type=str, help='name of enterprises',default='')
    parser.add_argument('-o', type=str, help='outpath windows must use Absolute path such as Y:\Tailorfinder\\test',dest='outpath',default='')
    parser.add_argument('-d' ,type=str,help='the path of domain file you can define your domain file dont use its domain file',dest='domain_path',default='')
    parser.add_argument('-p', type=int, help='the lowest percent of inversted company if you do not want collect input such as 101   ', dest='percent', default=100)
    parser.add_argument('-t', type=int, help='The number of days between custom collections starts', dest='time', default=0)
    parser.add_argument('-c', type=bool, help='isCollectSubdomain default is False', dest='collect', default=False)
    parser.add_argument('-fc', type=int, help='The number of branches,default is 5', dest='fcount',
                        default=5)
    parser.add_argument('-ps', type=bool, help='Whether to scan for ports default is False', dest='portscan',
                        default=False)
    parser.add_argument('-pf', type=str, help='The default path for port scanning is the xlsx is_alive table', dest='portfile',
                        default='')
    parser.add_argument('-iscdn', type=bool, help='Whether to check cdn default is False', dest='iscdn',
                        default=False)

    args = parser.parse_args()


    if args.name =='':
        colorprint.Red("[-]you must input -name example")
        sys.exit(0)

    if args.portscan == True and args.collect == False:
        Portscan.Port_Scan(args.outpath, args.name, args.portfile)



    if args.outpath =='':
        colorprint.Red("[-]you must input -o outpath")
        sys.exit(0)
    else:
        if not os.path.exists(args.outpath):
            os.mkdir(args.outpath)

        if args.time >0:
            #创建数据库
            CreateDatabase(args.name)
            while True:
                if args.domain_path != '':
                    CollectSubdomain(args.domain_path, args.outpath, args.name,args.iscdn)
                else:
                    findallDomain(args.name, args.outpath, args.percent,args.fcount)
                    if args.collect == True:
                        CollectSubdomain(args.outpath + "/domain", args.outpath, args.name,args.iscdn)
                        if args.portscan == True:
                            Portscan.Port_Scan(args.outpath, args.name,args.portfile)
                HandleTable(args.outpath, args.name)

                time.sleep(args.time*3600*24)

        else:
            if args.domain_path != '':
                CollectSubdomain(args.domain_path, args.outpath, args.name,args.iscdn)
                if args.portscan== True:
                    Portscan.Port_Scan(args.outpath, args.name, args.portfile)
            else:
                findallDomain(args.name,args.outpath,args.percent,args.fcount)
                if args.collect==True:
                    CollectSubdomain(args.outpath + "/domain", args.outpath, args.name,args.iscdn)
                    if args.portscan == True:
                        Portscan.Port_Scan(args.outpath, args.name, args.portfile)
