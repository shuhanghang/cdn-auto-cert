import pytest
from utils.cdn_handler.type import ProviderCdnModel, ProviderDnsModel, ProvidersModel


def test_dns_provider_name():
    with pytest.raises(ValueError) as e:
        ProviderCdnModel(cdnProvider='aliyun', dns=[ProviderDnsModel(provider='alidns',domains=['www.baidu.com']), ProviderDnsModel(provider='alidns',domains=['img.baidu.com'])])
    print(e.value)

def test_cdn_provider_name():
    with pytest.raises(ValueError) as e:
        a = ProviderCdnModel(cdnProvider='aliyun', dns=[ProviderDnsModel(provider='alidns',domains=['www.baidu.com']), ProviderDnsModel(provider='huawei',domains=['img.baidu.com'])])
        b = ProviderCdnModel(cdnProvider='aliyun', dns=[ProviderDnsModel(provider='alidns',domains=['www.baidu.com']), ProviderDnsModel(provider='R3',domains=['img.baidu.com'])])
        ProvidersModel(spec=[a,b])
    print(e.value)


def test_cdn_provider_name_range():
    with pytest.raises(ValueError) as e:
        a = ProviderCdnModel(cdnProvider='aliyun', dns=[ProviderDnsModel(provider='alidns', caProvider='zerossl',  domains=['www.baidu.com']), ProviderDnsModel(provider='huawei',domains=['img.baidu.com'])])
        b = ProviderCdnModel(cdnProvider='huawei1', dns=[ProviderDnsModel(provider='alidns', caProvider='zerossl', domains=['www.baidu.com']), ProviderDnsModel(provider='R3',domains=['img.baidu.com'])])
        ProvidersModel(spec=[a,b])
    print(e.value)
