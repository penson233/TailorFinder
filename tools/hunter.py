from config import hunter_key,hunter_name,hunterwb,huntersearch
from tools import colorprint
import base64
import requests
import time
import datetime






def hunterscan(domain,alldomain):

    hunterwb.append(["url","ip","port","web_title","domain","number","company"])
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d+%H:%M:%S')

    page = 1
    host = domain.replace('\n', '')
    query = huntersearch.format(host)

    search = base64.urlsafe_b64encode(query.encode("utf-8")).decode().replace('=','')
    all=0

    while True:
        url = f"https://hunter.qianxin.com/openApi/search?username={hunter_name}&api-key={hunter_key}&search={search}&start_time=2022-09-13+00%3A00%3A00&end_time={nowtime}&page={page}&page_size=100"
        r = requests.get(url=url,verify=False).json()
        if r['data']==None:
            colorprint.Green(f"\n[+] found {all} in {domain}")
            break

        if r['data']['arr']!=None:
            page += 1
            all+=len(r['data']['arr'])
            for i in r['data']['arr']:
                if i["domain"] not in alldomain:
                    alldomain.append(i["domain"])

                hunterwb.append([i['url'],
                                 i["ip"],
                                 i["port"],
                                 i["web_title"],
                                 i["domain"],
                                 i["number"],
                                 i["company"]
                                 ])

            time.sleep(30)
        else:
            colorprint.Green(f"\n[+] found {all} in {domain}")
            break
