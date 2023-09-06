import os
import uuid
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkdomain.request.v20180129.QueryDomainListRequest import QueryDomainListRequest
from aliyunsdkcdn.request.v20180510.DescribeUserDomainsRequest import DescribeUserDomainsRequest
from aliyunsdkdcdn.request.v20180115.DescribeDcdnUserDomainsRequest import DescribeDcdnUserDomainsRequest
from aliyunsdkcdn.request.v20180510.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest

from configs import *
from log import logger
from .provider import CdnProvider
from utils.checker.type import CdnDomainModel


class ALiyunCert(CdnProvider):
    def __init__(self):
        self.credentials = AccessKeyCredential(
            os.getenv('accessKey'), os.getenv('accessSecret'))
        self.client = AcsClient(region_id='cn-chengdu',
                                credential=self.credentials)
        self.certs_list = []
        self.name = "aliyun_cdn"
        self.cdn_dns_list: list[CdnDomainModel] = []
        self.dcdn_dns_list: list[CdnDomainModel] = []

    def recreate_request(self):
        self.request = ""
        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('cas.aliyuncs.com')
        self.request.set_protocol_type('https')
        self.request.set_version('2018-07-13')
        self.request.add_query_param('SourceIp', "0.0.0.0")
        self.request.add_query_param('Lang', "中文")

    def get_ssl_cert(self):
        """获取证书列表
           return: [{'name': 'test-shuhanghang-test-cert', 'endDate': '2022-07-12', 'id': 7598096}]
        """
        self.recreate_request()
        self.request.set_method('POST')
        self.request.set_action_name('DescribeUserCertificateList')
        self.request.add_query_param('ShowSize', "500")
        self.request.add_query_param('CurrentPage', "1")
        response = self.client.do_action(self.request)
        cert_list = json.loads(
            str(response, encoding='utf-8'))["CertificateList"]
        for i in cert_list:
            self.certs_list.append(
                {"name": i["name"], "endDate": i["endDate"], "id": i["id"]})
        return self.certs_list

    def upload_cert_for_cdn(self, domain, cert, key):
        """上传证书到aliyun cdn 对应域名下, 并开启https
        Args:
            domain (str): domain dict
            cert (str): cert
            key (str): key
        Returns:
            dict: {"RequestId":"***","CertId":*}
        """
        if domain[0:2] == "*.":
            self.domain = domain[1:]
        else:
            self.domain = domain
        self.cert = cert
        self.key = key
        self.cert_name = domain.replace(".", "-")+"-cert"
        self.delete_ssl_cert()
        self.recreate_request()
        self.request = SetDomainServerCertificateRequest()
        self.request.set_DomainName(self.domain)
        self.request.set_CertName(self.cert_name)
        self.request.set_CertType("upload")
        self.request.set_ServerCertificate(self.cert)
        self.request.set_PrivateKey(self.key)
        self.request.set_ServerCertificateStatus("on")
        res_json = json.loads(
            str(self.client.do_action_with_exception(self.request), encoding='utf-8'))
        logger.success(
            f"{self.name}: 为加速域名 {self.domain} 添加自定义上传证书 {self.cert_name}, {res_json}" + "\n")

    def delete_ssl_cert(self):
        """从证书管理服务中删除证书
        """
        self.certs_list = []
        self.get_ssl_cert()
        self.recreate_request()
        for cert in self.certs_list:
            if cert["name"] == self.cert_name:
                self.request.set_method('POST')
                self.request.set_action_name('DeleteUserCertificate')
                self.request.add_query_param('CertId', cert["id"])
                self.client.do_action(self.request)
                return True
        return False

    def get_dns_from_cdn(self):
        """从cdn域名管理中获取正在被使用的域名
           return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        self.recreate_request()
        self.request = DescribeUserDomainsRequest()
        self.request.set_PageSize(500)
        self.request.set_PageNumber(1)
        self.cdn_dns_list = []
        res_json = json.loads(
            str(self.client.do_action_with_exception(self.request), encoding='utf-8'))
        for cdn_dns in res_json["Domains"]["PageData"]:
            if cdn_dns["SslProtocol"] == "on":
                if cdn_dns["DomainName"][0] == '.':
                    domain_dict = {"domainName": cdn_dns["DomainName"], "SslProtocol": cdn_dns["SslProtocol"], "Cname": cdn_dns["Cname"],
                                   "DomainStatus": cdn_dns["DomainStatus"], "normalDns": "*" + cdn_dns["DomainName"], "type": "aliyun_cdn",
                                   "checkDomain": str(uuid.uuid1()) + cdn_dns["DomainName"]}

                    self.cdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))
                else:
                    domain_dict = {"domainName": cdn_dns["DomainName"], "SslProtocol": cdn_dns["SslProtocol"], "Cname": cdn_dns["Cname"],
                                   "DomainStatus": cdn_dns["DomainStatus"], "normalDns": cdn_dns["DomainName"], "type": "aliyun_cdn",
                                   "checkDomain": cdn_dns["DomainName"]}
                    self.cdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))
        return self.cdn_dns_list

    def get_dns_from_dcdn(self):
        """从dcdn域名管理中获取正在被使用的域名
           return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        self.recreate_request()
        self.request = DescribeDcdnUserDomainsRequest()
        self.request.set_PageSize(500)
        self.request.set_PageNumber(1)
        self.dcdn_dns_list = []
        self.response = self.client.do_action_with_exception(self.request)
        res_json = json.loads((str(self.response, encoding='utf-8')))
        for dcdn_dns in res_json["Domains"]["PageData"]:
            if dcdn_dns["SSLProtocol"] == "on":
                if dcdn_dns["DomainName"][0] == '.':
                    domain_dict = {"domainName": dcdn_dns["DomainName"], "SslProtocol": dcdn_dns["SSLProtocol"], "Cname": dcdn_dns["Cname"],
                                   "DomainStatus": dcdn_dns["DomainStatus"], "normalDns": "*" + dcdn_dns["DomainName"], "type": "aliyun_dcdn",
                                   "checkDomain": str(uuid.uuid1()) + dcdn_dns["DomainName"]}
                    self.dcdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))
                else:
                    domain_dict = {"domainName": dcdn_dns["DomainName"], "SslProtocol": dcdn_dns["SSLProtocol"], "Cname": dcdn_dns["Cname"],
                                   "DomainStatus": dcdn_dns["DomainStatus"], "normalDns": dcdn_dns["DomainName"], "type": "aliyun_dcdn",
                                   "checkDomain": dcdn_dns["DomainName"]}
                    self.dcdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))

        return self.dcdn_dns_list

    def get_dns_from_provider(self):
        self.get_dns_from_cdn()
        self.get_dns_from_dcdn()
        return self.cdn_dns_list + self.dcdn_dns_list
