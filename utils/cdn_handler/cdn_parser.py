import yaml
from log import logger
from configs import providers_config
from .type import ProvidersModel, ProviderCdnModel


def parsing_config() -> list[ProviderCdnModel]:
    """解析providers.yml
    """
    try:
        with open(providers_config, "r") as providers_file:
            providers_data = providers_file.read()
            providers_dict = yaml.load(providers_data, Loader=yaml.FullLoader)
            return ProvidersModel.model_validate(providers_dict).spec

    except Exception as e:
        logger.error(f"配置文件: 解析yaml文件错误，{e}")
        raise e


providers = parsing_config()

def get_dns_provider(domain: str):
    """获取配置文件中dns供应商名"""
    for cdn_field in providers:
        for dns_field in cdn_field.dns:
            if [i for i in dns_field.domains if i in domain]:
                return (dns_field.provider)
    return ''


def get_ca_provider(cdn_provider_name: str, dns_provider_name: str):
    """获取配置文件中ca供应商名"""
    for cdn_field in providers:
        if cdn_field.cdnProvider == cdn_provider_name:
            for dns_field in cdn_field.dns:
                if dns_field.provider == dns_provider_name:
                    return dns_field.caProvider
    return ''
