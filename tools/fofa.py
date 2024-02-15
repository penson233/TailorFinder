import re

from config import FOFA_EMAIL,FOFA_KEY,fofawb
import time
from tools.commons import readdomain
import base64
import requests

def fofascan(file,alldomain):
    domains = readdomain(file)

    fofawb.append(["domain", 'header_code', 'ip', 'port', 'webtitle'])
    fofa_ip=''
    for i in domains:
        page = 1
        host = i.replace('\n', '')
        query = f"domain=\"{host}\"||cert=\"{host}\""
        print(query)

        q = base64.b64encode(query.encode()).decode()
        while True:
            url = f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={q}&fields=domain,host,title,ip,port,server&size=1000&page={page}"
            print(url)
            r = requests.get(url=url).json()

            if not r['error']:

                if len(r['results']) != 0:
                    for i in r['results']:
                        
                        fofawb.append(i[1:])
                        if i[0]!="":
                            alldomain.append(i[1])
                        else:
                            fofa_ip+=i[3]+'\n'
                    page += 1
                    time.sleep(2)
                else:
                    break
            else:
                break
    return fofa_ip
