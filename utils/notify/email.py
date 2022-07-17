import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config import *


def send_email(dns_provider_name, domain, expire_days):
    mail_msg = f"""
    <p>CDN提供商：{domain['type']}</p>
    <p>DNS提供商：{dns_provider_name}</p>
    <p>加速域名： {domain['domainName']}</p>
    <p>检查URL：<a href="https://{domain['fqdn']}" target="_blank">{domain['fqdn']}</a></p>
    <p>事件：<span style="color:red">{expire_days} 天后过期，请手动更新</span></p>
    """
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(MAIL_USER, 'utf-8')
    message['To'] = Header(";".join(RECEIVERS), 'utf-8')

    subject = f"加速域名 {domain['domainName']} HTTPS证书即将过期"
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(MAIL_HOST, 25)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(SENDER, RECEIVERS, message.as_string())
        return True
    except Exception:
        return False
