from config import assetfinderwb
from tools.commons import readdomain
from tools.systemcmd import runshell
from tools import colorprint

def assetfinderscan(file,outpath,alldomain,platform):
    assetfinderwb.append(["子域名"])
    if platform == "linux":
        cmd = "cat %s | xargs -I {} ./bin/assetfinder/assetfinder {} >> %s/assetfinder.txt" %(file, outpath)
        runshell(cmd, "assetfinder")
    elif platform =="darwin":
        cmd = "cat %s | xargs -I {} ./bin/assetfinder/assetfinder_m {} >> %s/assetfinder.txt" % (file, outpath)
        runshell(cmd, "assetfinder")

    elif platform == "win32" or platform == "win64":
        domains=readdomain(file)
        for domain in domains:
            cmd="cd bin/assetfinder && assetfinder.exe %s >> %s/assetfinder.txt" % (domain.replace('\n',''),outpath)
            runshell(cmd,"assetfinder")

    with open(outpath+"/assetfinder.txt",'r') as f:
        read=f.readlines()

    domains = ''.join(readdomain(file)).split('\n')
    for domain in domains:
        for i in read:
            if domain in i:
                print(i)
                alldomain.append(i.replace('\n',''))
                assetfinderwb.append([i.replace('\n','')])