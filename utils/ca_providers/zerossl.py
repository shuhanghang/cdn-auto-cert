from configs import *
from utils.ca_providers.provider import CAProvider

class ZerosslCA(CAProvider):
    def __init__(self, dns_provider_name, domain):
        self.ca_name = "zerossl"
        self.dns_provider_name = dns_provider_name
        self.domain = domain

    @property
    def cmd(self):
        return rf"""lego --email {EMAIL} \
        --dns {self.dns_provider_name} \
        --domains {self.domain} \
        --path {CERT_PATH} \
    	--server https://acme.zerossl.com/v2/DV90 \
        --eab \
        --kid $ZeroSSL_KID \
        --hmac $ZeroSSL_HMAC \
    	-a run"""
