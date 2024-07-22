from config import rappidnswb
from tools import colorprint
from bs4 import BeautifulSoup
import requests


def rappidnssearch(domain,alldomain):
    rappidnswb.append(['子域名'])
    header={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    url=f"https://rapiddns.io/s/{domain}?full=1"
    try:
        r=requests.get(url,headers=header)
        soup = BeautifulSoup(r.text, "html.parser")

        trs=soup.find_all("table")[0].find_all('tbody')[0].find_all('tr')
        colorprint.Green(f"\n[+] found {len(trs)} in {domain}")

        for tr in trs:
            tds=tr.find_all('td')
            if tds[0].text not in alldomain:
                alldomain.append(tds[0].text)
            rappidnswb.append([tds[0].text])

    except Exception as e:
        print(f"\n[-] no found {len(trs)} in {domain}")


