#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 11:37
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    :
# @File    : main.py
# @Software: PyCharm

import argparse
import sys
from tools import colorprint
from functions import findallDomain,CollectSubdomain

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TailorFinder powered by penson\nA asset collection tool for Chinese enterprises\n such as\n\npython3 main.py -name 王尼玛有限公司 -p 100 -o ./test/')
    parser.add_argument('-name', type=str, help='name of enterprises')
    parser.add_argument('-o', type=str, help='outpath windows must use Absolute path such as Y:\Tailorfinder\\test',dest='outpath',default='')
    parser.add_argument('-d' ,type=str,help='the path of domain file you can define your domain file dont use its domain file',dest='domain_path',default='')
    parser.add_argument('-p', type=int, help='the lowest percent of inversted company if you do not want collect input such as 101   ', dest='percent', default=100)
    
    args = parser.parse_args()

    if args.outpath =='':
        colorprint.Red("[-]you must input -o outpath")
        sys.exit(0)

    if args.domain_path != '':
        CollectSubdomain(args.domain_path, args.outpath, args.name)
    else:
        findallDomain(args.name,args.outpath,args.percent)

        CollectSubdomain(args.outpath + "/domain", args.outpath, args.name)


