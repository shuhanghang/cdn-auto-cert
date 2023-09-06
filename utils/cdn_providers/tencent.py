
import os
import json
import uuid

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ssl.v20191205 import ssl_client, models as ssl_models
from tencentcloud.cdn.v20180606 import cdn_client, models as cdn_modles

from log import logger
from .provider import CdnProvider
from utils.checker.type import CdnDomainModel


class TencentCert(CdnProvider):
    def __init__(self):
        self.credentials = credential.Credential(
            os.getenv('SecretId'), os.getenv('SecretKey'))
        self.http_profile = HttpProfile()
        self.http_profile.enpoint = "ssl.tencentcloudapi.com"
        self.client_profile = ClientProfile()
        self.client_profile.httpProfile = self.http_profile
        self.client = ssl_client.SslClient(
            self.credentials, "", self.client_profile)
        self.certs_list = []
        self.name = "tencent_cdn"
        self.cdn_dns_list: list[CdnDomainModel] = []

    def recreate_request(self):
        self.http_profile.enpoint = "cdn.tencentcloudapi.com"
        self.client_profile.httpProfile = self.http_profile
        self.client = cdn_client.CdnClient(
            self.credentials, "", self.client_profile)

    def get_ssl_cert(self):
        """获取证书列表
            return: [{'name': 'test-shuhang-xyz-cert', 'endDate': '2022-07-12', 'id': 7598096}]
        """
        req = ssl_models.DescribeCertificatesRequest()
        resp = json.loads(
            self.client.DescribeCertificates(req).to_json_string())
        if resp["TotalCount"] != 0:
            for i in resp["Certificates"]:
                self.certs_list.append(
                    {"name": i["Alias"], "endDate": i["CertEndTime"], "id": i["CertificateId"]})
        return self.certs_list

    def upload_cert_for_cdn(self, domain, cert, key):
        """上传证书到cdn, 不托管证书"""
        if domain[0:2] == "*.":
            self.domain = domain[1:]
        else:
            self.domain = domain
        self.cert = cert
        self.key = key
        self.cert_alias = domain.replace(".", "-")+"-cert"
        # self.delete_ssl_cert()
        self.recreate_request()
        req = cdn_modles.UpdateDomainConfigRequest()
        params = {
            "Domain": self.domain,
            "Https": {
                "Switch": "on",
                "CertInfo": {
                    "Certificate": cert,
                    "PrivateKey": key,
                    "Message": self.cert_alias
                }
            }
        }
        req.from_json_string(json.dumps(params))
        resp = self.client.UpdateDomainConfig(req).to_json_string()
        logger.success(
            f"{self.name}: 为加速域名 {self.domain} 添加自定义上传证书 {self.cert_alias}, {resp}" + "\n")

    def delete_ssl_cert(self):
        """从证书管理服务中删除证书
        """
        self.certs_list = []
        self.get_ssl_cert()
        for cert in self.certs_list:
            if cert["name"] == self.cert_alias:
                req = ssl_models.DeleteCertificateRequest()
                params = {
                    "CertificateId": cert["id"]
                }
                req.from_json_string(json.dumps(params))
                resp = self.client.DeleteCertificate(req)
                if json.loads(resp.to_json_string())["DeleteResult"] == "true":
                    return True
        return False

    def get_dns_from_cdn(self):
        return self.cdn_dns_list

    def get_dns_from_ecdn(self):
        return self.cdn_dns_list

    def get_dns_from_provider(self) -> list[CdnDomainModel]:
        self.recreate_request()
        req = cdn_modles.DescribeDomainsRequest()
        params = {
        }
        req.from_json_string(json.dumps(params))
        resp = json.loads(self.client.DescribeDomains(req).to_json_string())
        for cdn_dns in resp["Domains"]:
            if cdn_dns["Status"] == "online":
                if cdn_dns["Domain"][0] == '*':
                    domain_dict = {"domainName": cdn_dns["Domain"], "SslProtocol": "NaN", "Cname": cdn_dns["Cname"],
                                   "DomainStatus": cdn_dns["Status"], "normalDns": cdn_dns["Domain"], "type": "tencent_" + cdn_dns["Product"],
                                   "checkDomain": str(uuid.uuid1()) + cdn_dns["Domain"][1:]}
                    self.cdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))
                else:
                    domain_dict = {"domainName": cdn_dns["Domain"], "SslProtocol": "NaN", "Cname": cdn_dns["Cname"],
                                   "DomainStatus": cdn_dns["Status"], "normalDns": cdn_dns["Domain"], "type": "tencent_" + cdn_dns["Product"],
                                   "checkDomain":  cdn_dns["Domain"]}
                    self.cdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))

        return self.cdn_dns_list
