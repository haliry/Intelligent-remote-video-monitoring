#coding=utf8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

_user = "xxx@qq.com"
_pwd = "xxx"
_to = "xxx@qq.com"

def send():
    msg = MIMEMultipart('related')
    msg["Subject"] = "家里情况警报！！！"
    msg["From"] = _user
    msg["To"] = _to

    part = MIMEText("树莓派监测到家里有运动物体，附件中是当前家里环境的截图，详细情况请前往网站查看！")
    msg.attach(part)

    with open('/home/pi/Downloads/stream-video-browser/img/p.jpg','rb') as f:
        part = MIMEApplication(f.read())
        part.add_header('Content-Disposition','attachment',filename='fire.jpg')
        msg.attach(part)

    s = smtplib.SMTP("smtp.qq.com",port=25,timeout=100)
    s.ehlo()
    s.starttls()
    s.login(_user,_pwd)
    s.sendmail(_user,_to,msg.as_string())
    s.close()

