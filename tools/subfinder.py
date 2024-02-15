from config import subfinderwb

from tools.systemcmd import runshell

def subfinderscan(file,outpath,alldomain,platform):
    subfinderwb.append(["子域名"])
    if platform =="linux":
        cmd ="./bin/subfinder/subfinder -dL %s -o %s/subfinder.txt" % (file, outpath)
        runshell(cmd, "subfinder")

    elif platform =="darwin":
        cmd="./bin/subfinder/subfinder_m -dL %s -o %s/subfinder.txt" %(file,outpath)
        runshell(cmd, "subfinder")

 
    elif platform == "win32" or platform == "win64":
        print(outpath)
        cmd="cd bin/subfinder/ && subfinder.exe -dL %s -o %s/subfinder.txt" %(file,outpath)
        runshell(cmd,"subfinder")




    with open(outpath+"/subfinder.txt",'r') as f:
        read=f.readlines()
    for i in read:
        alldomain.append(i.replace('\n',''))
        subfinderwb.append([i.replace('\n','')])


