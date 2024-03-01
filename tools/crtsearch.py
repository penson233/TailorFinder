import requests
from bs4 import BeautifulSoup
from config import  crtwb
from tools import colorprint


def CrtSearch(domain,alldomain):
    crtwb.append(["domain"])


    try:
        url="https://crt.sh/?q={}".format(domain.replace("\n",""))

        r=requests.get(url)
        soup=BeautifulSoup(r.text, "html.parser")

        table=soup.find_all("table")[1].find("td").find("table").find_all("tr")

        colorprint.Green(f"\n[+] found {len(table)} in {domain}")
        for i in table:
            td=i.find_all("td")
            if len(td) >0:
                if '*.' not in td[5].text:
                    td = str(td[5]).replace("<td>", "").replace("</td>", "").split("<br/>")
                    if len(td) > 1:
                        for t in td:
                            if t not in alldomain:
                                alldomain.append(t)
                            crtwb.append([t])
                    else:
                        crtwb.append([td[0]])
                        if td[0] not in alldomain:
                            alldomain.append(td[0])

    except:
        print("\n[-]{} no found".format(domain.replace("\n","")))
