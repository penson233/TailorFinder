import requests
from bs4 import BeautifulSoup
from tools.commons import readdomain
from config import  crtwb


def CrtSearch(file,alldomain):
    domains = readdomain(file)
    crtwb.append(["domain"])


    for doamin in domains:
        try:
            url="https://crt.sh/?q={}".format(doamin.replace("\n",""))

            r=requests.get(url)
            soup=BeautifulSoup(r.text, "html.parser")

            table=soup.find_all("table")[1].find("td").find("table").find_all("tr")

            for i in table:
                td=i.find_all("td")
                if len(td) >0:
                    if '*.' not in td[5].text:
                        td = str(td[5]).replace("<td>", "").replace("</td>", "").split("<br/>")
                        if len(td) > 1:
                            for t in td:
                                print(t)
                                alldomain.append(t)
                                crtwb.append([t])
                        else:
                            crtwb.append([td[0]])
                            alldomain.append(td[0])
                            print(td[0])

        except:
            crtwb.append(["{} no found".format(doamin.replace("\n",""))])
