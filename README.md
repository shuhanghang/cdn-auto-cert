# CDN证书自动更新

## 1. 环境
+ python3.9.6
+ [acme.sh](https://github.com/acmesh-official/acme.sh)

## 2. 说明
1. 在线获取CDN正在使用的加速域名（**CNAME正确配置、开启HTTPS**）
2. 在线检测站点证书过期时间（满足设定阈值触发报警或尝试申请证书）
3. 调用acme.sh脚本重新申请证书、上传更新到对应cdn供应商上对应加速域名使用的证书

## 3. 配置
1. 公共配置文件：[config.py](./config/config.py)
2. CDN-DNS配置文件: [providers.yml](./config/providers.yml)
```yaml
# dnsProvider(DNS供应商)目前支持： aliyun (阿里云)、dnsPod (腾讯云)、huawei(华为云)、cloudFlare
# cdnProvider(CDN提供商)目前支持： aliyun (阿里云)、tencent (腾讯云)
Providers:
- cdnProvider: aliyun
  description: "CDN或DCDN提供商是阿里云，使用的加速域名提供商是阿里云、腾讯云"
  providerKey:
    accessKey: ""
    accessSecret: ""
  dns:
    - provider: aliyun
      providerKey:
        accessKey: ""
        accessSecret: ""
      domains:
        - test1.com
        - test2.cn
    - provider: dnsPod
      providerKey:
        DP_Id: "" 
        DP_Key: ""
      domains:
        - "test1.net"

- cdnProvider: tencent
  description: "CDN或ECDN提供商是腾讯云，使用的加速域名提供商是cloudFlare、华为"
  providerKey:
    SecretId: ""
    SecretKey: ""
  dns:
    - provider: cloudFlare
      providerKey:
        CF_Key: ""
        CF_Email: "test@test.com"
      domains:
        - test1.xyz
    - provider: huawei
      providerKey:
        HUAWEICLOUD_Username: ""
        HUAWEICLOUD_Password: ""
        HUAWEICLOUD_ProjectID: ""
      domains:
        - test1.io
```

## 4. 运行
### 1. 手动
``` shell
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
python3 cdn_auto_cert.py
```
### 2. 定时 
```
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
python3 cdn_auto_cert_scheduler.py
```
### 3. docker
```shell
docker build -t cdn-auto-cert:latest .
docker --name auto-cert -it -v $PWD/config/config.py:/home/config/config.py && \
       -v $PWD/config/providers.yml:/home/config/providers.yml && \
       -d cdn-auto-cert:latest
```
> <p style="color:red">运行前先配置好 **config.py** 和 **providers.yml**<p>
> <strong>使用前请检查加速域名是否开启https并配置正确cname，否则检查不通过不会自动更新</strong>