from config import subfinderwb

from tools.systemcmd import runshell
from config import l_subfinder,m_subfinder
from tools import colorprint

def subfinderscan(file,outpath,alldomain,platform):
    subfinderwb.append(["子域名"])
    if platform =="linux":
        cmd =l_subfinder.format(file, outpath)
        runshell(cmd, "subfinder")

    elif platform =="darwin":
        cmd=  m_subfinder.format(file,outpath)
        runshell(cmd, "subfinder")


    with open(outpath+"/subfinder.txt",'r') as f:
        read=f.readlines()



    for i in read:
        if i.replace('\n','') not in alldomain:
            alldomain.append(i.replace('\n',''))
            subfinderwb.append([i.replace('\n','')])

    colorprint.Green(f"\n[+] collect {len(read)} domain")

