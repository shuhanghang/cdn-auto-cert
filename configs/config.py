# 证书下载目录
CERT_PATH = '/tmp/cert'
# 证书签发注册邮箱
EMAIL ='yourEmail@example.com'

# 自动申请证书触发天数EXPIRE_MAX，当证书过期时间小于该值时触发，默认提前30天
EXPIRE_MAX = 30
EXPIRE_MIN = 0

# 证书服务运行crontab
AUTO_CERT_CRON = '30 23 * * * '

# 公共DNS，https检查用
PUBLIC_DNS = ['223.5.5.5','223.6.6.6']

# 证书过期触发报警发送邮件时间点（剩余天）
CERT_EXPIRE_ALERT = [15, 10, 6, 3, 2, 1]

# 报警邮箱配置
ALERT = True
MAIL_HOST = 'smtp.server.com'
MAIL_USER = 'yourEmail@example.com'
MAIL_PASS = 'yourEmailPass'
MAIL_SENDER = 'SenderEmail@example.com'
MAIL_RECEIVERS = ['ReceiversEmail@example.com']

# UI 登录
UI_USER = 'admin'
UI_PASS = 'admin'