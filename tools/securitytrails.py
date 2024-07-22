import requests
from tools import colorprint
from config import securitykey,securitytrailswb



def securscan(domain,alldomain):


    securitytrailswb.append(["domains"])
    domain=domain.replace("\n","")
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": securitykey
    }

    try:
        response = requests.get(url, headers=headers).json()


        subdomains=response["subdomains"]
        if(len(subdomains) >0):
            colorprint.Green(f"\n[+] found {len(subdomains)} in {domain}")
            for i in subdomains:
                subdomain = i + "." + domain
                try:
                    if subdomain not in alldomain:
                        alldomain.append(subdomain)
                    securitytrailswb.append([subdomain])
                except Exception as e:
                    print("\nerror: "+i+"."+domain+" "+e.__str__()+"\n")
                    securitytrailswb.append(['error_domain: '+subdomain])
        else:
            print(f"\n[-] no found in {domain}")
    except Exception as e:
        print(f"\n[-] no found in {domain}")



