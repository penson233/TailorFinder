from config import hunter_key,hunter_name,hunterwb,huntersearch
from tools import colorprint
import base64
import requests
import time
import datetime




def hunterscan(domain,alldomain,outpath):
    host = domain.replace('\n', '')
    query = huntersearch.format(host)

    search = base64.urlsafe_b64encode(query.encode("utf-8")).decode().replace('=','')

    task_id=huntergettask(search)
    if task_id!=0:
        while True:
            if gettaskstatus(task_id):
                gettaskdetail(task_id, alldomain, domain,outpath)
                break
            else:
                continue






#获取下载任务
def huntergettask(search):
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
    url = f"https://hunter.qianxin.com/openApi/search/batch?api-key={hunter_key}&search={search}&is_web=1&start_time=2022-09-13&end_time={nowtime}"

    r = requests.post(url=url, verify=False).json()
    print(r)
    task_id=0
    if r['data'] !=None:
        if "task_id" not in r["data"]:
            return task_id
        else:
            task_id=r["data"]["task_id"]

    return task_id

#查看是否可以下载
def gettaskstatus(task_id):
    while True:
        r=requests.get(f"https://hunter.qianxin.com/openApi/search/batch/{str(task_id)}?api-key={hunter_key}",verify=False)
        result=r.json()
        if result["code"] ==200:
            if result["data"]["status"]=="已完成":
                return True
            else:
                continue
        else:
            print(result)

#获取hunter查询结果
def gettaskdetail(task_id,alldomain,domain,outpath):

    r=requests.get(f"https://hunter.qianxin.com/openApi/search/download/{task_id}?api-key={hunter_key}",verify=False)
    with open(f"{outpath}/hunteroutput_{domain}.csv","w")as f:
        f.write(r.text)

    repeat=[]
    outputcsv=r.text.split('\n')
    colorprint.Green(f"\n[+] found {len(outputcsv)-1} in {domain}")
    for i in range(1,len(outputcsv)):
        result=outputcsv[i].split(',')
        if len(result)>1:
            hunterwb.append(result)
            if result[2] not in repeat and result[2]!="":
                repeat.append(result[2])
                if result[2] not in alldomain:
                    alldomain.append(result[2])

