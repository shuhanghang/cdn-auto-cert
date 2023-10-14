# zerossl密钥
## 默认值为空
## 使用zerossl申请证书时指定，参考 https://ffis.me/archives/2110.html/comment-page-3
## 当使用其他机构申请的证书上传到cdn报证书链错误时，推荐使用zerossl申请证书
ZeroSSL_KID = ""
ZeroSSL_HMAC = ""


# cdn 供应商api访问秘钥变量
## tencent
SecretId = ""
SecretKey = ""
## aliyun
accessKey = ""
accessSecret = ""
## huawei
ak = ""
sk = ""


# dns 供应商api访问秘钥变量 (名称参考 https://go-acme.github.io/lego/dns/)
## aliyun
ALICLOUD_ACCESS_KEY = ""
ALICLOUD_SECRET_KEY = ""
