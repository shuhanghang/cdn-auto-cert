from pydantic import BaseModel, field_validator
from utils.ca_providers import ca_providers
from utils.cdn_providers import cdn_providers

class ProviderDnsModel(BaseModel):
    provider: str
    caProvider: str = 'letsencrypt'
    domains: list[str]

    @field_validator('caProvider')
    @classmethod
    def cdn_provider(cls, ca_provier_name: str):
        if ca_provier_name.strip() == '':
            return 'letsencrypt'
        ca_providers_name_list = ca_providers.instance.keys()
        if not ca_provier_name in ca_providers_name_list:
             raise ValueError(f'配置文件错误: ca供应商名 {ca_provier_name} 不在 {ca_providers_name_list}中')
        return ca_provier_name


class ProviderCdnModel(BaseModel):
    cdnProvider: str
    description: str = ''
    dns: list[ProviderDnsModel]

    @field_validator('cdnProvider')
    @classmethod
    def cdn_provider(cls, cdn_provider_name: str):
        cdn_providers_name_list = cdn_providers.instance.keys()
        if not cdn_provider_name in cdn_providers_name_list:
             raise ValueError(f'配置文件错误: cdn供应商名 {cdn_provider_name} 不在 {cdn_providers_name_list}中')
        return cdn_provider_name


    @field_validator('dns')
    @classmethod
    def cdn_dns_name_connot_repeat(cls, dns_filed_list: list[ProviderDnsModel]):
        dns_provider_list = [dns_filed.provider for dns_filed in dns_filed_list]
        if len(set(dns_provider_list)) != len(dns_provider_list):
             raise ValueError('配置文件错误: 一个cdn供应商下不能包含多个相同的dns供应商')
        return dns_filed_list
    
class ProvidersModel(BaseModel):
    spec: list[ProviderCdnModel]

    @field_validator('spec')
    @classmethod
    def cdn_name_connot_repeat(cls, cdn_filed_list: list[ProviderCdnModel]):
        cdn_provider_list = [cdn_filed.cdnProvider for cdn_filed in cdn_filed_list]
        if len(set(cdn_provider_list)) != len(cdn_provider_list):
             raise ValueError('配置文件错误: 不能包含多个相同的cdn供应商')
        return cdn_filed_list
