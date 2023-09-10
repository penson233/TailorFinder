from config import rappidnswb
from tools.commons import readdomain
from bs4 import BeautifulSoup
import requests


def rappidnssearch(file,alldomain):
    domains = readdomain(file)
    rappidnswb.append(['子域名'])
    for domain in domains:
        header={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }

        url=f"https://rapiddns.io/s/{domain}?full=1"
        r=requests.get(url,headers=header)


        soup = BeautifulSoup(r.text, "html.parser")

        trs=soup.find_all("table")[0].find_all('tbody')[0].find_all('tr')
        replace=[]
        for tr in trs:
            tds=tr.find_all('td')
            if tds[0].text not in replace:
                print(tds[0].text)
                rappidnswb.append([tds[0].text])
                alldomain.append(tds[0].text)
                replace.append(tds[0].text)
