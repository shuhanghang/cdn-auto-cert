import yaml
from log import logger

from config import *
from log import logger
from utils.cdn.aliyun import ALiyunCdn
from utils.cdn.tencent import TencentCdn

class CdnConfig():
    """处理yml配置文件中获取正在使用的cdn列表"""

    def __init__(self, cdn_conf):
        self.conf = cdn_conf
        self.name = cdn_conf["cdnProvider"]
        self.key = cdn_conf["providerKey"]
        self.get_dns_config()

    def get_dns_config(self):
        """读取每个cdn列表下的dns配置"""
        if dns_config:= self.conf["dns"]:
            self.dns_config = dns_config
        else:
            self.dns_config = []

    @property
    def provider(self):
        """返回cdn供应商对象"""
        if self.name == "aliyun":
            return ALiyunCdn(self.key)
        elif self.name == "tencent":
            return TencentCdn(self.key)
    
    
def get_providers_config():
    """解析providers.yml"""
    try:
        with open(providers_config, "r", encoding='utf-8') as providers_file:
            providers_data = providers_file.read()
            providers_dict = yaml.load(providers_data, Loader = yaml.FullLoader)
            return providers_dict["Providers"]

    except Exception as e:
        logger.error(f"providers: 解析yaml文件错误; msg:{e}")
        return []
