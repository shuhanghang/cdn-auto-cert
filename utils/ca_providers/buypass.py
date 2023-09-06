from configs import *
from utils.ca_providers.provider import CAProvider

class BuypassCA(CAProvider):
    def __init__(self, dns_provider_name, domain):
        self.ca_name = "buypass"
        self.dns_provider_name = dns_provider_name
        self.domain = domain
    
    @property
    def cmd(self):
        return f"lego --email {EMAIL} --dns {self.dns_provider_name} --domains {self.domain} --path {CERT_PATH} --server https://api.buypass.com/acme/directory -a run"
