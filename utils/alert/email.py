import smtplib
from email.mime.text import MIMEText
from email.header import Header

from configs import *
from utils.checker.type import CdnDomainModel

def send_notification(dns_provider_name: str, domain: CdnDomainModel, expire_days: int):
    """发送邮件通知
    """
    body = f"""
    <p>CDN提供商：{domain.type}</p>
    <p>DNS提供商：{dns_provider_name}</p>
    <p>加速域名： {domain.domainName}</p>
    <p>检查URL：<a href="https://{domain.checkDomain}" target="_blank">{domain.checkDomain}</a></p>
    <p>事件：<span style="color:red">{expire_days} 天后过期，请手动更新</span></p>
    """
    message = MIMEText(body, 'html', 'utf-8')
    message['From'] = Header(MAIL_USER, 'utf-8')
    message['To'] =  Header(";".join(MAIL_RECEIVERS), 'utf-8')
    
    subject = f"加速域名 {domain.domainName} HTTPS证书即将过期"
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(MAIL_HOST, 25)
        smtpObj.login(MAIL_USER, MAIL_PASS)  
        smtpObj.sendmail(MAIL_SENDER, MAIL_RECEIVERS, message.as_string())
        return True
    except Exception:
        return False