from config import hunter_key,hunter_name,hunterwb
from tools.commons import readdomain
import base64
import requests
import time
import datetime





def hunterscan(file,alldomain):

    domains = readdomain(file)
    hunterwb.append(["url","ip","port","web_title","domain","number","company"])
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d+%H:%M:%S')
    for i in domains:
        page = 1
        host = i.replace('\n', '')
        query = f'domain="{host}"'
        print(query)

        search = base64.urlsafe_b64encode(query.encode("utf-8")).decode().replace('=','')


        while True:
            url = f"https://hunter.qianxin.com/openApi/search?username={hunter_name}&api-key={hunter_key}&search={search}&start_time=2022-09-13+00%3A00%3A00&end_time={nowtime}&page={page}&page_size=100"
            print(url)
            r = requests.get(url=url,verify=False).json()
            if r['data']==None:
                break

            if r['data']['arr']!=None:
                page += 1
                for i in r['data']['arr']:
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
                break
