from config import assetfinderwb
from tools.commons import readdomain
from tools.systemcmd import runshell
from config import l_assetfinder,m_assetfinder
from tools import colorprint

def assetfinderscan(file,outpath,alldomain,platform):
    assetfinderwb.append(["子域名"])
    if platform == "linux":
        cmd = l_assetfinder %(file, outpath)
        runshell(cmd, "assetfinder")
    elif platform =="darwin":
        cmd = m_assetfinder % (file, outpath)
        runshell(cmd, "assetfinder")

    with open(outpath+"/assetfinder.txt",'r') as f:
        read=f.readlines()

    domains = ''.join(readdomain(file)).split('\n')

    for domain in domains:
        for i in read:
            if domain in i:
                if i not in alldomain:
                    alldomain.append(i.replace('\n',''))
                assetfinderwb.append([i.replace('\n','')])
    colorprint.Green(f"\n[+] collect {len(read)} domain")