from openpyxl import Workbook
#fofa
FOFA_EMAIL = ""
FOFA_KEY = ""


#hunter
hunter_key=""
hunter_name=""


#天眼查
tyccookie=""
tyctoken=""
#veryvp http://veryvp.com/
veryvpcookie=""
#爱奇查
aqccookie=""
#securitytrails
securitykey=""

#https://hunter.io
hunteremailkey=""


##设置持续话收集邮箱

emailaccount = ""
emailpassword = ""
emailtarget=['']
mailhost=""


wb = Workbook()

wb.create_sheet("domain",0)
wb.create_sheet("company_structs",1)
wb.create_sheet("旗下app",2)
wb.create_sheet("email",3)
wb.create_sheet("subfinder", 4)
wb.create_sheet("fofa", 5)
wb.create_sheet("hunter",6)
wb.create_sheet("crt.sh",7)
wb.create_sheet("assetfinder",8)
wb.create_sheet("shuffledns",9)
wb.create_sheet("securitytrails", 10)
wb.create_sheet("rappidns",11)
wb.create_sheet("ip138",12)
wb.create_sheet("alldomain",13)



rootdomain=wb["domain"]
emailwb=wb["email"]
appwb=wb["旗下app"]
subfinderwb = wb["subfinder"]
fofawb=wb["fofa"]
hunterwb=wb["hunter"]
crtwb=wb["crt.sh"]
ctwb=wb["company_structs"]
assetfinderwb=wb["assetfinder"]
alldomainwb=wb["alldomain"]
shufflednswb=wb["shuffledns"]
securitytrailswb=wb["securitytrails"]
rappidnswb=wb["rappidns"]
ip138wb=wb["ip138"]

#fofa查询语法
fofasearch= "domain=\"{}\"||cert=\"{}\""

#hunter查询语法
huntersearch='domain="{}"'



#工具参数
#shuffledns
#linux
l_shuffledns="cat %s | xargs -I {} ./bin/shuffledns/shuffledns -d {} -w ./bin/shuffledns/domain.txt -r ./bin/shuffledns/resolvers.txt  >> %s/shuffledns.txt -m ./bin/massdns/massdns_linux"
#macos
m_shuffledns="cat %s | xargs -I {} ./bin/shuffledns/shuffledns -d {} -w ./bin/shuffledns/domain.txt -r ./bin/shuffledns/resolvers.txt  >> %s/shuffledns.txt -m ./bin/massdns/massdns_linux"


#assetfinder
#linux
l_assetfinder="cat %s | xargs -I {} ./bin/assetfinder/assetfinder {} >> %s/assetfinder.txt"
#macos
m_assetfinder="cat %s | xargs -I {} ./bin/assetfinder/assetfinder_m {} >> %s/assetfinder.txt"



#subfinder
#linux
l_subfinder="./bin/subfinder/subfinder -dL {} -o {}/subfinder.txt"
#mac
m_subfinder="./bin/subfinder/subfinder_m -dL {} -o {}/subfinder.txt"

#端口扫描参数 预留格式化参数{} outpath
masscan="masscan -iL {}/alive_ip.txt -p 1-65535 --rate=1000 -oJ {}/alive_port.json"

#nmap扫描部分参数
nmap="-sV -n --open -Pn -sT -T4 --version-intensity 7"