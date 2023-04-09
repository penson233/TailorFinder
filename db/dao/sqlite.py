#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 11:09
# @Author  : penson
# @email   ：decentpenson@gmail.com
# @Site    : 
# @File    : sqlite.py
# @Software: PyCharm


import hashlib
import sqlite3
from tools.commons import sendemail
def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def DbConnect():
    dbPath = 'db/domains.db'
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    return conn,cursor

def ExitTable(name):
    conn,cursor= DbConnect()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (str(md5(name)),))
    result = cursor.fetchone()
    if result:
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False


def CreateTable(name):
    conn,cursor =DbConnect()
    if not ExitTable(name):
        cursor.execute(f'''create table {md5(name)}
                  (domain text not null)''')
        cursor.close()
        conn.commit()
        conn.close()

def SelectTable(name):
    conn, cursor = DbConnect()
    cursor.execute(f"select domain from {md5(name)}")

    return cursor

def InsertTable(alldomain,name):
    conn,cursor=DbConnect()
    rows=[]
    for j in SelectTable(name):
        rows.append(j[0])
    count=0

    for i in alldomain:
        if i not in rows:
            print(i)
            cursor.execute(f"insert into {md5(name)} (domain) values ('{i}')")
            count+=1

    sendemail(f"搜索更新到{str(count)}个域名")
    conn.commit()
    conn.close()


