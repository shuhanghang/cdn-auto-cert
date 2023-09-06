# 使用zerossl请求证书时指定，参考 https://ffis.me/archives/2110.html/comment-page-3
# 当申请证书上传到cdn报证书链错误时，推荐使用zerossl

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