
import os

from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
from huaweicloudsdkcdn.v1 import *
from huaweicloudsdkeps.v1 import ListEnterpriseProjectRequest, EpsClient
from huaweicloudsdkeps.v1.region.eps_region import EpsRegion

from log import logger
from .provider import CdnProvider
from utils.checker.type import CdnDomainModel


class HuaweiCert(CdnProvider):
    def __init__(self):
        self.credentials = GlobalCredentials(os.getenv('ak'), os.getenv('sk'))
        self.client = CdnClient.new_builder().with_credentials(
            self.credentials).with_region(CdnRegion.value_of("cn-north-1")).build()
        self.name = "huawei_cdn"
        self.cdn_dns_list: list[CdnDomainModel] = []
        self.project_domains_list = []
        self.project_certs_list = []
        self.project_id_list = []
        self.certs_list = []
        self.get_project_id_list()
        self.get_project_domain_cert_list()

    def get_project_id_list(self):
        self.eps_client = EpsClient.new_builder() \
            .with_credentials(self.credentials) \
            .with_region(EpsRegion.value_of("cn-north-4")) \
            .build()
        response = self.eps_client.list_enterprise_project(
            ListEnterpriseProjectRequest())
        for project in response.enterprise_projects:
            self.project_id_list.append(project.id)

    def get_project_domain_cert_list(self):
        cert_request = ShowCertificatesHttpsInfoRequest()
        domain_request = ListDomainsRequest()
        for project_id in self.project_id_list:
            cert_request.enterprise_project_id = project_id
            domain_request.enterprise_project_id = project_id
            certs_response = self.client.show_certificates_https_info(
                cert_request)
            domains_response = self.client.list_domains(domain_request)
            if domains_response.total > 0:
                self.project_domains_list = self.project_domains_list + domains_response.domains
                self.project_certs_list = self.project_certs_list + certs_response.https

    def get_ssl_cert(self):
        """获取证书列表
            return: [{'name': 'test-shuhang-xyz-cert', 'endDate': '2022-07-12', 'id': 7598096}]
        """
        return self.certs_list

    def upload_cert_for_cdn(self, domain, cert, key):
        """上传证书到 cdn 对应域名下
        """
        for https in self.project_certs_list:
            if https.domain_name == domain:
                request = UpdateHttpsInfoRequest()
                request.domain_id = self.get_dns_id_from_cdn(domain)
                httpsHttpInfoRequestBody = HttpInfoRequestBody(
                    cert_name=https.cert_name,
                    https_status=https.https_status,
                    certificate=cert,
                    private_key=key,
                    http2=https.http2,
                    certificate_type=https.certificate_type,
                    force_redirect_https=https.force_redirect_https,
                    force_redirect_config=https.force_redirect_config
                )
                request.body = HttpInfoRequest(
                    https=httpsHttpInfoRequestBody
                )
                self.client.update_https_info(request)
                logger.success(
                    f"{self.name}: 为加速域名 {domain} 添加自定义上传证书 {https.cert_name}" + "\n")

    def get_dns_from_cdn(self):
        """从cdn域名管理中获取正在被使用的域名
            return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        return self.cdn_dns_list

    def get_dns_from_dcdn(self):
        """从全站加速域名管理中获取正在被使用的域名
            return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        return self.dcdn_dns_list

    def get_dns_id_from_cdn(self, domain):
        """获取加速域名
        """
        for cdn_dns in self.project_domains_list:
            if cdn_dns.domain_name == domain:
                return cdn_dns.id

    def get_dns_from_provider(self) -> list[CdnDomainModel]:
        for https in self.project_certs_list:
            for cdn_dns in self.project_domains_list:
                if cdn_dns.domain_name == https.domain_name:
                    domain_dict = {"domainName": https.domain_name, "SslProtocol": "true", "Cname": cdn_dns.cname,
                                   "DomainStatus": cdn_dns.domain_status, "normalDns": https.domain_name, "type": "huawei_cdn",
                                   "checkDomain": https.domain_name}
                    self.cdn_dns_list.append(
                        CdnDomainModel.model_validate(domain_dict))
        return self.cdn_dns_list
