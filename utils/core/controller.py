from threading import Thread

from utils.core.configurator import CdnConfig, get_providers_config
from utils.cert.manager import CertManager

cdns_config = get_providers_config()


def cdn_dns_handler() -> list[CertManager]:
    """获取待申请证书的对象"""
    jobs_list = []
    for cdn_config in cdns_config:
        cdn_config_obj = CdnConfig(cdn_config)  # 获取cdn处理器对象
        cdn_domains = cdn_config_obj.provider.check_cdn()  # 通过检查的加速域名
        # 遍历cdn下不同的dns提供商配置
        for dns_config in cdn_config_obj.dns_config:
            # 遍历cdn使用的加速域名
            for cdn_domain in cdn_domains:
                # 遍历dns配置下domains配置
                for dns_domain in dns_config["domains"]:
                    # 匹配加速域名
                    if dns_domain == ".".join(cdn_domain["domainName"].split(".")[-2:]):
                        cert = CertManager(
                            cdn_domain, dns_config, cdn_config_obj.name)
                        if cert.check_expire:
                            jobs_list.append(cert)
    return jobs_list


def cert_handler(cert_jobs_list: list[CertManager]):
    """多线程证书申请和上传"""
    for cert_job in cert_jobs_list:
        Thread(target=cert_job.run).start()


def main():
    """程序入口"""
    cert_jobs_list = cdn_dns_handler()
    cert_handler(cert_jobs_list)
