
from utils.checker.type import CdnDomainModel


class CdnProvider():
    def __init__(self):
        pass

    def get_ssl_cert(self):
        """获取证书列表
           return: [{'name': 'test-test-com-cert', 'endDate': '2023-11-23', 'id': 7598096}]
        """
        pass

    def upload_cert_for_cdn(self, domain: str, cert: str, key: str):
        """上传证书到 cdn 对应域名下, 并开启https
        """
        pass

    def delete_ssl_cert(self):
        """从证书管理服务中删除证书
        """
        pass

    def get_dns_from_cdn(self) -> list[CdnDomainModel]:
        """从cdn域名管理中获取正在被使用的域名
           return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        self.cdn_dns_list: list[CdnDomainModel] = []
        return self.cdn_dns_list

    def get_dns_from_dcdn(self) -> list[CdnDomainModel]:
        """从全站加速域名管理中获取正在被使用的域名
           return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
        """
        self.dcdn_dns_list: list[CdnDomainModel] = []
        return self.dcdn_dns_list

    def get_dns_from_provider(self) -> list[CdnDomainModel]:
        self.get_dns_from_cdn()
        self.get_dns_from_dcdn()
        return self.cdn_dns_list + self.dcdn_dns_list


class CdnProviderFactory():
    def __init__(self):
        self.instance = {}

    def registry(self, name: str, provider_cls: type[CdnProvider]):
        self.instance[name] = provider_cls

    def get(self, name: str) -> CdnProvider:
        if instance := self.instance[name]:
            return instance()
        return CdnProvider()