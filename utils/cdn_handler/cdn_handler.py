import timeout_decorator

from configs import *
from log import logger
from .type import ProviderCdnModel
from utils.checker import cname_check
from utils.cdn_providers import CdnProvider, cdn_providers

class CdnProviderHandler():
    """获取cdn正在使用的加速域名列表"""

    def __init__(self, cdn_provider: CdnProvider):
        self.cdn_provider = cdn_provider

    @timeout_decorator.timeout(60*30, use_signals=False)
    def cdn_domain_cname_check(self):
        """检查cdn供应商下正确配置cname的域名

        Returns:
            List : 返回cdn供应商下cname配置正确的域名列表
        """
        try:
            cdn_domains = self.cdn_provider.get_dns_from_provider()
            checked_domains = cname_check(cdn_domains)
            return checked_domains
        except Exception as e:
            logger.error(f"cdn加速域名cname检查: 执行失败，{e}")
            raise e

class CdnConfigHandler():
    """处理yml配置文件中获取正在使用的cdn列表"""

    def __init__(self, cdn_provider_conf: ProviderCdnModel):
        """
        Args:
            cdn_provider_config (ProviderCdnModel): cdn对象
        """
        self.cdn_dns_config = []
        self.cdn_provider_conf = cdn_provider_conf
        self.cdn_provider_name = cdn_provider_conf.cdnProvider

        self.cdn_config_handler()

    def cdn_config_handler(self):
        """读取每个cdn列表下的 dns 配置"""
        if cdn_dns_config := self.cdn_provider_conf.dns:
            self.cdn_dns_config = cdn_dns_config

    @property
    def cdn_provider(self):
        """返回cdn供应商对象"""
        return cdn_providers.get(self.cdn_provider_name)
