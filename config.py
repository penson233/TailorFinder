from openpyxl import Workbook

#fofa
FOFA_EMAIL = ""
FOFA_KEY = ""


#hunter
hunter_key=""
hunter_name=""


#天眼查
tyccookie=""

#veryvp
veryvpcookie=""

#爱奇查
aqccookie=''

#securitytrails
securitykey=""

#https://hunter.io
hunteremailkey=""

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
wb.create_sheet("alldomain",12)


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