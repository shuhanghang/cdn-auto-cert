
# ACME
# ACME脚本路径
ACME_PATH = "/root/.acme.sh/acme.sh"
# 证书下载目录
ACME_CERT_PATH = '/tmp/cert'
# 证书签发提供商列表
ACME_CERT_SERVER = ["https://api.buypass.com/acme/directory", "zerossl"]
# 证书签发注册邮箱
EMAIL = 'register@exmple.com'

# 自动申请证书触发天数EXPIRE_MAX，默认提前30天
EXPIRE_MAX = 30
EXPIRE_MIN = 0

# 证书服务运行crontab
AUTO_CERT_CRON = '0 7 * * *'

# 公共DNS
PUBLIC_DNS = ['223.5.5.5','223.6.6.6']

# 证书过期触发报警发送邮件时间点（剩余天）
CERT_EXPIRE_ALERT = [25, 20, 10, 5, 3, 2, 1]

# 报警邮箱配置
MAIL_ENABLE = True
MAIL_HOST = "smtp.xxx.com"
MAIL_USER = "exmple@exmple.com"
MAIL_PASS = "XXXXXX"  
SENDER = "exmple@exmple.com"
RECEIVERS = ["exmple1@exmple.com", "exmple2@exmple.com"]
