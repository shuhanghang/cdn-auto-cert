from utils.cdn_providers.aliyun import ALiyunCert
from utils.cdn_providers.huawei import HuaweiCert
from utils.cdn_providers.tencent import TencentCert
from utils.cdn_providers.provider import CdnProviderFactory, CdnProvider

cdn_providers = CdnProviderFactory()

cdn_providers.registry("aliyun", ALiyunCert)
cdn_providers.registry("huawei", HuaweiCert)
cdn_providers.registry("tencent", TencentCert)


__all__ = ['cdn_providers', 'CdnProvider']
