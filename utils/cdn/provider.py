import timeout_decorator
from abc import ABCMeta, abstractmethod

from utils.checker import check_cdn_cname


class CdnProvider(metaclass=ABCMeta):
    """cdn提供商证书服务基类"""
    
    @abstractmethod
    def __init__(self):
        self.credentials = ""
        self.client = ""
        self.certs_list = []
        self.name = ""

    @abstractmethod
    def get_ssl_cert(self) -> list:
        """获取证书列表"""
        pass

    @abstractmethod
    def upload_cert_to_cdn(self, domain, cert ,key) -> None: 
        """上传证书到 cdn 对应域名下, 并开启https"""
        pass

    @abstractmethod
    def delete_ssl_cert(self) -> bool:
        """从证书管理服务中删除证书"""
        pass
    
    def get_dns_from_cdn(self) -> list:
        """从加速域名管理中获取正在被使用的域名列表"""
        pass
    
    def get_dns_from_dcdn(self) -> list:
        """从全站加速域名管理中获取正在被使用的域名列表"""
        pass

    @abstractmethod
    def get_dns_from_provider(self) -> list:
        """从CDN域名管理中获取正在被使用的所有域名列表"""
        pass
    
    @timeout_decorator.timeout(60*30, use_signals=False)
    def check_cdn(self):
        """检查cdn中开启https并正确配置cname的加速域名"""
        cdn_domains = self.get_dns_from_provider()
        checked_domains = check_cdn_cname(cdn_domains)
        return checked_domains