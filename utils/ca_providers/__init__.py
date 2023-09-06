from utils.ca_providers.buypass import BuypassCA
from utils.ca_providers.letsencrypt import LetsencryptCA
from utils.ca_providers.zerossl import ZerosslCA
from utils.ca_providers.provider import CAProviderFactory,CAProvider

ca_providers = CAProviderFactory()
ca_providers.registry('buypass', BuypassCA)
ca_providers.registry('letsencrypt', LetsencryptCA)
ca_providers.registry('zerossl', ZerosslCA)


__all__ = ['ca_providers','CAProvider']
