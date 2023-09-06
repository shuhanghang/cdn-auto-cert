from log import logger
from configs import cert_handler_list
from utils.cert_handler.main import CertHandler
from utils.cdn_handler.cdn_parser import providers
from utils.cdn_handler.cdn_handler import CdnConfigHandler, CdnProviderHandler
from utils.checker.type import CheckedCnameModel

cert_handler_list: list[CertHandler]

def check_cdn_all_cname():
    """检查所有加速域名cname"""
    logger.info("cdn检查: ·所有·开启https并配置cname的域名")
    # 遍历cdn提供商配置
    for provider_cdn in providers:
        cdn_handler = CdnConfigHandler(provider_cdn)
        cdn_provider = CdnProviderHandler(cdn_handler.cdn_provider)
        cdn_domains = cdn_provider.cdn_domain_cname_check()
        help_cert_handler(cdn_handler, cdn_domains)


def help_cert_handler(cdn_handler: CdnConfigHandler, cdn_domains: list[CheckedCnameModel]):
    """变量配置文件生成域名对象添加到cert_handler_list列表"""
    # 遍历cdn下不同的dns提供商配置
    for dns_provider_conf in cdn_handler.cdn_dns_config:
        # 遍历cdn使用的加速域名
        for cdn_domain in cdn_domains:
            for dns_provider_domain in dns_provider_conf.domains:
                if dns_provider_domain in cdn_domain.domainName:
                    cert = CertHandler(
                        cdn_domain, dns_provider_conf, cdn_handler.cdn_provider)
                    cert_handler_list.append(cert)

def check_cdn_dns_health():
    """检查目标域名证书状态"""
    global cert_handler_list
    _cert_handler_list = []
    logger.info("健康检查: 在线检查·目标域名·健康状态")
    for cert in cert_handler_list:
        if cert.check_cert_online:
            _cert_handler_list.append(cert)

    cert_handler_list = _cert_handler_list

def run_cdn_cert_job():
    """cdn证书申请和上传"""
    res = ''
    for _ in range(len(cert_handler_list)):
        job = cert_handler_list.pop()
        res = job.apply_cert()
    return res