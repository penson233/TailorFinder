from config import emailaccount,emailtarget,emailpassword,mailhost
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

#读取文件
def readdomain(filepath):
    with open(filepath,'r') as f:
        read = f.readlines()
    return read


def sendemail(content):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html'))
    # 配置调用邮件信息
    msg['Subject'] = 'TailorFinder收集结果'  # 设置邮件主题
    msg['From'] = "TailorFinder"  # 设置发件人


    s = smtplib.SMTP_SSL(mailhost, 465)
    s.login(emailaccount, emailpassword)
    for i in emailtarget:
        msg['To'] = i  # 设置收件人
        s.sendmail(emailaccount, i, msg.as_string())