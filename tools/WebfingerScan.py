#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/1/19 11:11
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : WebfingerScan.py
# @Software: PyCharm
import json
import re
import codecs
import requests
from chardet.universaldetector import UniversalDetector
import chardet

def to_utf8(content, content_type):
    html_encode = "gb18030"
    html_encode2 = ""
    html_encode3 = ""

    if "gbk" in content_type or "gb2312" in content_type or "gb18030" in content_type or "windows-1252" in content_type:
        html_encode = "gb18030"
    elif "big5" in content_type:
        html_encode = "big5"
    elif "utf-8" in content_type:
        # 实际上，这里获取的编码未必是正确的，在下面还要做比对
        html_encode = "utf-8"
    # 使用正则表达式提取<meta>标签中的charset信息
    meta_charset = re.compile(r'(?is)<meta[^>]*charset\s*=["\']?\s*([A-Za-z0-9\-]+)')
    match = meta_charset.search(content)
    if match:
        content_type = match.group(1).lower()
        if "gbk" in content_type or "gb2312" in content_type or "gb18030" in content_type or "windows-1252" in content_type:
            html_encode2 = "gb18030"
        elif "big5" in content_type:
            html_encode2 = "big5"
        elif "utf-8" in content_type:
            html_encode2 = "utf-8"

    # 使用正则表达式提取<title>标签中的内容，并通过chardet库获取编码信息
    title_charset = re.compile(r'(?is)<title[^>]*>(.*?)<\/title>')
    match = title_charset.search(content)
    if match:
        title_text = match.group(1)
        encoding = chardet.detect(title_text.encode())['encoding']
        if encoding !=None:
            content_type = encoding.lower()

        if 'gbk' in content_type or 'gb2312' in content_type or 'gb18030' in content_type or 'windows-1252' in content_type:
            html_encode = "gb18030"
        elif 'big5' in content_type:
            html_encode = "big5"
        elif 'utf-8' in content_type:
            html_encode = "utf-8"

    if html_encode != "" and html_encode2 != "" and html_encode != html_encode2:
        html_encode = html_encode2

    if html_encode == "utf-8" and html_encode != html_encode3:
        html_encode = html_encode3

    if html_encode != "" and html_encode != "utf-8":
        content = convert(content, html_encode, "utf-8")



    return content

def convert(src, src_code, tag_code):
    if src_code == tag_code:
        return src
    src_bytes = src.encode(src_code)  # 将源字符串编码为字节流
    src_result = src_bytes.decode(src_code)  # 将字节流解码为字符串
    tag_bytes = codecs.encode(src_result, tag_code)  # 将解码后的字符串按目标编码重新编码为字节流
    result = tag_bytes.decode(tag_code)  # 将字节流解码为字符串
    return result


def findtitle(response):

    # 使用正则表达式提取网页标题
    title_pattern = re.compile(r'<title>(.*?)</title>')
    title_match = title_pattern.search(response)

    # 检查是否找到标题
    if title_match:
        title = title_match.group(1)

    else:
        title="None"
    return title

def check_keywords(string, keywords):
    # 检查字符串中是否同时包含所有关键字
    return all(keyword in string for keyword in keywords)


def Scan(target,resp,fingerjson,content_type):
    resptext = to_utf8(resp.text, content_type)
    resptitle=findtitle(resptext)

    fingerlist=[]
    for finger in fingerjson:

        if "request" not in finger:
            if finger["method"] == "keyword":
                if finger['location'] == 'title':
                    if check_keywords(resptitle, finger['keyword']):
                        print(target, finger)
                        fingerlist.append(finger)
                elif finger['location'] == 'body':
                    if check_keywords(resptext, finger['keyword']):
                        print(target, finger)
                        fingerlist.append(finger)
                elif finger['location'] == 'header':
                    if check_keywords(str(resp.headers), finger['keyword']):
                        print(target, finger)
                        fingerlist.append(finger)


        else:
            if finger["request"]["method"] == "GET":
                response = requests.get(f"{target}/{finger['request']['path']}",
                                        headers=finger["request"]['headers'], data=finger["request"]['body'], timeout=5,
                                        verify=False, allow_redirects=True)
                try:
                    context_type = response.headers["Content-Type"]
                except:
                    context_type = ""
                response_t = to_utf8(response.text, context_type)
                title_find = findtitle(response_t)
                if finger["method"] == "keyword":
                    if finger['location'] == 'title':
                        if check_keywords(title_find, finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)
                    elif finger['location'] == 'body':
                        if check_keywords(response_t, finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)
                    elif finger['location'] == 'header':
                        if check_keywords(str(resp.headers), finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)



            elif finger["request"]["method"] == "POST":
                response = requests.post(f"{target}/{finger['request']['path']}",
                                        headers=finger["request"]['headers'], data=finger["request"]['body'], timeout=5,
                                        verify=False, allow_redirects=True)
                try:
                    context_type = response.headers["Content-Type"]
                except:
                    context_type = ""
                response_t = to_utf8(response.text, context_type)
                title_find = findtitle(response_t)
                if finger["method"] == "keyword":
                    if finger['location'] == 'title':
                        if check_keywords(title_find, finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)
                    elif finger['location'] == 'body':
                        if check_keywords(response_t, finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)
                    elif finger['location'] == 'header':
                        if check_keywords(str(resp.headers), finger['keyword']):
                            print(target, finger)
                            fingerlist.append(finger)
    if len(fingerlist) == 0:
        print(target, "{'cms':'web'}")
        fingerlist.append({'cms': 'web'})
    return fingerlist
