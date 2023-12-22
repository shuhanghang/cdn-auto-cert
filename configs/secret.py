#zerossl密钥
##默认使用letsencrypt申请证书，若使用zerossl请指定其值
##开启教程参考 https://ffis.me/archives/2110.html/comment-page-3
##获取的`EAB Kid`对应ZeroSSL_KID，`EAB HMAC Key`对应ZeroSSL_HMAC
##当使用其他机构申请的证书上传到cdn报证书链错误时，推荐使用zerossl申请证书
##zerossl申请证书默认会有证书过期邮件告警，避免重复告警请关闭zerossl上的过期告警
ZeroSSL_KID = ""
ZeroSSL_HMAC = ""


#cdn 供应商api访问秘钥
##tencent
##腾讯云cdn供应商，若使用请指定其值
##获取教程参考 https://www.anhengcloud.com/help/publiccloud/qcloud/qcloud-accesskey.html
SecretId = ""
SecretKey = ""

##aliyun
##阿里云cdn供应商，若使用请指定其值
##获取教程参考 https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair
##获取的`AccessKey ID`对应accessKey，`AccessKey Secret`对应accessSecret
accessKey = ""
accessSecret = ""

##huawei
##华为云cdn供应商，若使用请指定其值
##获取教程参考 https://support.huaweicloud.com/intl/zh-cn/usermanual-ca/ca_01_0003.html
ak = ""
sk = ""


#dns 供应商api访问秘钥
##变量名参考 https://go-acme.github.io/lego/dns/
##变量值参考 对应cdn供应商api密钥
##aliyun
ALICLOUD_ACCESS_KEY = ""
ALICLOUD_SECRET_KEY = ""
