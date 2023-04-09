import re
from tools import colorprint
from tools.subfinder import subfinderscan
from tools.assetfinder import assetfinderscan
from tools.shuffledns import shufflednsscan
from tools.fofa import fofascan
from tools.hunter import hunterscan
from tools.securitytrails import securscan
from tools.rappidns import rappidnssearch
from tools.huntermail import hunterfindemail
from tools.formatEmail import formatemailFind
from config import *
from tools.IPgather import readxls
from tools.crtsearch import CrtSearch
from tools.veryvp import veryvpfind
from tools import tyc
from db.dao.sqlite import CreateTable,InsertTable
from tools import aqc
import sys



def filter(text):
    text=re.sub("http://|https://","",text)
    return text



def allDomain(alldomain,out_path):
    domain_isreal=[]
    place = re.compile("http://|https://|\n|:\d+")
    for i in alldomain:
        target = place.sub("", i)
        if target not in domain_isreal:
            domain_isreal.append(target)

    alldomainwb.append(["alldomain"])
    with open(out_path+'/alldomain.txt','w') as f:
        for domain in domain_isreal:
            f.write(domain+"\n")
            alldomainwb.append([domain])


def findallDomain(name,outpath,percent):

    tycresult,tycchildren=tyc.findalldomain(name,percent)
    aqcresult,aqcchildren,appresult=aqc.findalldomain(name,percent)

    rootdomain.append(['描述','域名','icp备案号','来源'])
    ctwb.append(['子公司','占股','金额',"来源"])
    appwb.append(['app名称','app类别','简介','所属公司'])


    repeat=''

    for childty in tycchildren:
        ctwb.append([childty[0],childty[3],childty[1],"天眼查"])

    for childaq in aqcchildren:
        ctwb.append([childaq[0], childaq[2], childaq[3],"爱企查"])

    for i in tycresult:
        rootdomain.append(i)
        repeat+=i[1]+"\n"

    for j in aqcresult:
        rootdomain.append(j)

        repeat += j[1] + "\n"

    for k in appresult:
        appwb.append(k)


    e=''

    ipreg = re.compile("\d+\.\d+\.\d+\.\d+")
    with open(outpath+"/domain",'w') as f:
        for t in repeat.split('\n'):
            if t not in e:
                print(t)
                if not ipreg.match(t):
                    f.write(t + "\n")
                    e += t
                else:
                    with open(outpath+"/ipfind.txt","a+") as fa:
                        fa.write(t+"\n")


    colorprint.Green("\n[+]Gathered successfully! ! ! ! saved in "+outpath+'/domain and '+outpath+'/ipfind.txt')


    colorprint.Red("\n[-]Gathering email....")
    findemail(outpath+'/domain')
    colorprint.Green("\n[+]Gathered email over")


def findemail(domain_file):
    with open(domain_file,"r") as f:
        read=f.readlines()
    emailwb.append(["邮箱", "来源"])
    allemail=[]
    for i in read:

        veryvpfind(i.replace('\n',''),allemail)
        hunterfindemail(i.replace('\n',''),allemail)
        formatemailFind(i.replace('\n',''),allemail)



def CollectSubdomain(domain_file,out_path,name):


    alldomain=[]
    platform=sys.platform


    colorprint.Red("\n[-]Gathering subdomains......")

    '''crt'''
    colorprint.Red("[-]using crt....")
    CrtSearch(domain_file,alldomain)

    '''rappidns'''
    colorprint.Red("[-]using rappidns....")
    rappidnssearch(domain_file,alldomain)

    '''securitytrails'''
    colorprint.Red("[-]using securitytrails....")
    securscan(domain_file,alldomain)


    '''fofa'''
    colorprint.Red("[-]using fofa....")
    fofascan(domain_file,alldomain)

    '''hunter'''
    colorprint.Red("[-]using hunter....")
    hunterscan(domain_file,alldomain)




    '''assetfinder'''
    colorprint.Red("[-]using assetfinder....")
    assetfinderscan(domain_file,out_path,alldomain,platform)

    '''subfinder'''
    colorprint.Red("[-]using subfinder....")
    subfinderscan(domain_file,out_path,alldomain,platform)

    '''shuffledns'''
    colorprint.Red("[-]using shuffledns to brute subdomains....")
    shufflednsscan(domain_file,out_path,alldomain,platform)


    colorprint.Green("[+]collect all subdomains successfully")

    allDomain(alldomain,out_path)


    wb.save(out_path+'/'+'test.xlsx')

    # '''fofa hunter c段收集统计'''
    readxls(out_path,name)
    colorprint.Green("[+]task finished")


def CreateDatabase(name):
    CreateTable(name)


def HandleTable(outpath,name):
    with open(outpath+"/alldomain.txt","r") as f:
        read=f.readlines()
    alldomain=','.join(read).replace('\n','').split(',')

    colorprint.Green("\n[-]try to insert "+str(len(alldomain))+" to table")
    InsertTable(alldomain,name)
