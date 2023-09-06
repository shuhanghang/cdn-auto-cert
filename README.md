# cdn-auto-cert
CDN HTTPS 证书自动更新，支持阿里云、腾讯云、华为云

## 1. 说明
1. 读取CDN正在使用的加速域名，获取正在使用（正确配置）且开启HTTPS的加速域名
2. 检测站点证书过期时间，满足设定阈值触发重新申请证书或报警（邮件）
3. 调用lego申请证书、上传更新到对应cdn供应商

## 2. 功能
+ 支持CDN加速域名证书定时检测、证书申请、证书上传
+ 支持多级域名、全域名匹配
+ 支持UI查看域名证书状态，手动更新状态和证书
+ 支持指定CA机构
+ 支持证书过期邮件通知
+ 支持命令行、Docker运行

## 3. 配置
1. 公共配置文件：[config.py](./configs/config.py)
2. CDN-DNS配置文件：[providers.yml](./configs/providers.yml)
3. 供应商秘钥文件：[secret.py](./configs/secret.py)

```yml
# cdnProvider(CDN提供商)支持: aliyun (阿里云)、tencent (腾讯云)、huawei(华为云)
# dnsProvider(DNS供应商)支持: 名称参考 https://go-acme.github.io/lego/dns/ 
# caProvider(CA供应商)支持:   letsencrypt（Let's Encrypt）、buypass（Buypass）、zerossl（ZeroSSL）
spec:
  - cdnProvider: aliyun
    description: "CDN提供商是阿里云，使用的加速域名提供商是阿里云、腾讯云"
    dns:
      - provider: alidns
        caProvider: ''    # 默认值为'letsencrypt'，也可以不写该字段
        domains:
          - test1.cn           # 二级域名
          - www.test2.com      # 全域名
      - provider: tencentcloud
        domains:
          - "test1.net"

  - cdnProvider: tencent
    description: "CDN提供商是腾讯云，使用的加速域名提供商是cloudFlare、route53"
    dns:
      - provider: cloudflare
        caProvider: "zerossl"
        domains:
          - test1.xyz
      - provider: route53
        domains:
          - test1.io

  - cdnProvider: huawei
    description: "CDN提供商是华为云，使用的加速域名提供商是阿里云、Google Cloud"
    dns:
      - provider: gcloud
        caProvider: "zerossl"
        domains:
          - test1.org
```
> 提示：
**添加新的CDN加速域名首次需手动开启https并手动上传证书**

## 4. 运行
### 1. 手动
``` shell
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
python3 auto_cert.py
```

### 2. 定时
```shell
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
python3 auto_cert_scheduler.py
```
---
支持面板，默认账号密码：admin/admin
```shell
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
python3 app.py
```
### 3. docker
```shell
docker build -t cdn-auto-cert:latest -f Dockerfiles/basic/Dockerfile .
docker --name cdn-auto-cert -it && \
  -v $PWD/config/config.py:/home/config/config.py && \
  -v $PWD/config/providers.yml:/home/config/providers.yml && \
  -v $PWD/config/secret.py:/home/config/secret.py && \
  -d cdn-auto-cert:latest
```
---
支持面板，默认账号密码：admin/admin
```shell
docker build -t cdn-auto-cert-ui:latest -f Dockerfiles/ui/Dockerfile .
docker --name cdn-auto-cert -it && \
  -p 8080:8080 && \
  -v $PWD/config/config.py:/home/config/config.py && \
  -v $PWD/config/providers.yml:/home/config/providers.yml && \
  -v $PWD/config/secret.py:/home/config/secret.py && \
  -d cdn-auto-cert-ui:latest
```

## 5. 截图
<div align="center">
  <img alt="cdn-auto-cert" src="./docs/images/screenshot.png">
  <p>日志</p>
  <img alt="cdn-auto-cert" src="./docs/images/ui.png">
  <p>面板</p>
</div>

## 6. 环境
+ python3.9.6^
+ [lego](https://github.com/go-acme/lego)
+ [layui](https://github.com/layui/layui)
