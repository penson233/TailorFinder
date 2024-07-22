from config import shufflednswb
from tools.systemcmd import runshell
from tools import colorprint
from config import l_shuffledns,m_shuffledns

def shufflednsscan(file,outpath,alldomain,platform):

    shufflednswb.append(["子域名"])
    if platform == "linux":
        cmd = l_shuffledns %(file, outpath)
        runshell(cmd, "shuffledns")
    elif platform =="darwin":
        cmd=m_shuffledns %(file,outpath)

        runshell(cmd, "shuffledns")

    with open(outpath + "/shuffledns.txt", 'r') as f:
        read = f.readlines()
    for i in read:
        if i.replace('\n', '') not in alldomain:
            alldomain.append(i.replace('\n', ''))
            shufflednswb.append([i.replace('\n', '')])

    colorprint.Green(f"\n[+] collect {len(read)} domain")

