from configs import *
from utils.ca_providers.provider import CAProvider


class LetsencryptCA(CAProvider):
    def __init__(self, dns_provider_name: str, domain: str):
        self.ca_name = "letsencrypt"
        self.dns_provider_name = dns_provider_name
        self.domain = domain
    
    @property
    def cmd(self):
        return f"lego --email {EMAIL} --dns {self.dns_provider_name} --domains {self.domain} --path {CERT_PATH} -a run"
