from config import emailaccount,emailtarget,emailpassword,mailhost
from email.mime.text import MIMEText
from email.header import Header
import smtplib
#读取文件
def readdomain(filepath):
    with open(filepath,'r') as f:
        read = f.readlines()
    return read


def sendemail(content):
    wymail = smtplib.SMTP()
    wymail.connect(mailhost, 25)
    wymail.login(emailaccount, emailpassword)
    # 输入你的邮件正文，为字符串格式


    message = MIMEText(content, 'plain', 'utf-8')

    subject = "TailorFinder"

    message['Subject'] = Header(subject, 'utf-8')
    wymail.sendmail(emailaccount, emailtarget, message.as_string())
