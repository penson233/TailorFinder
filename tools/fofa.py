import re

from config import FOFA_EMAIL,FOFA_KEY,fofawb,fofasearch
import time
from tools import colorprint
import base64
import requests

def fofascan(domain,alldomain):
    fofa_ip=''

    page = 1
    host = domain.replace('\n', '')
    query = fofasearch.format(host,host)

    q = base64.b64encode(query.encode()).decode()
    all=0

    while True:
        url = f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={q}&fields=domain,host,title,ip,port,server&size=1000&page={page}"
        r = requests.get(url=url).json()

        if not r['error']:
            all+=len(r['results'])
            if len(r['results']) != 0:
                for i in r['results']:
                    fofawb.append(i[1:])
                    if i[0]!="":
                        if i[1] not in alldomain:
                            alldomain.append(i[1])
                    else:
                        fofa_ip+=i[3]+'\n'
                page += 1
                time.sleep(2)
            else:
                colorprint.Green(f"\n[+] found {all} in {domain}")
                break
        else:
            colorprint.Green(f"\n[+] found {all} in {domain}")
            break
    return fofa_ip
