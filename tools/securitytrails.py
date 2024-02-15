import requests
from tools.commons import readdomain
from config import securitykey,securitytrailswb



def securscan(file,alldomain):


    domains = readdomain(file)
    securitytrailswb.append(["domains"])
    for domain in domains:
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

                for i in subdomains:
                    subdomain = i + "." + domain
                    try:
                        print(subdomain)
                        alldomain.append(subdomain)
                    except Exception as e:
                        print(e)
                        print("error: "+i+"."+domain+" "+e.__str__()+"\n")
                        securitytrailswb.append(['error_domain: '+subdomain])
        except:
            continue

