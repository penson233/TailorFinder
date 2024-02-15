from config import shufflednswb
from tools.systemcmd import runshell
from tools.commons import readdomain

def shufflednsscan(file,outpath,alldomain,platform):

    shufflednswb.append(["子域名"])
    if platform == "linux":
        cmd = "./bin/shuffledns/shuffledns -l %s -w ./bin/shuffledns/domain.txt -r ./bin/shuffledns/resolvers.txt -d {} >> %s/shuffledns.txt -m ./bin/massdns/massdns_linux" %(file, outpath)
        runshell(cmd, "shuffledns")
    elif platform =="darwin":
        cmd="./bin/shuffledns/shuffledns_m -l %s -w ./bin/shuffledns/domain.txt -r ./bin/shuffledns/resolvers.txt -d {} -m ./bin/massdns/massdns_mac >> %s/shuffledns.txt" %(file,outpath)
        runshell(cmd, "shuffledns")

    elif platform =="win32" or platform =="win64":
        domains = readdomain(file)
        for domain in domains:
            cmd="cd bin/shuffledns && shuffledns.exe -w domain.txt -r resolvers.txt -d %s -m ../massdns/massdns.exe >> %s/shuffledns.txt" %(domain.replace('\n',''),outpath)
            runshell(cmd, "shuffledns")


    with open(outpath + "/shuffledns.txt", 'r') as f:
        read = f.readlines()
    for i in read:
        alldomain.append(i.replace('\n', ''))
        shufflednswb.append([i.replace('\n', '')])

