import os

from config import *


class Acme():

    def __init__(self, dns_provider, domain: str):
        self.dns_provider = dns_provider
        self.domain = domain
        self.acme_path = ACME_PATH
        self.email = EMAIL
        self.cert_path = ACME_CERT_PATH
        self.set_acme_path()

    def set_acme_path(self):
        default_path = "/root/.acme.sh/acme.sh"
        if os.path.exists(default_path):
            self.acme_path = default_path
        if not os.path.exists(ACME_PATH):
            self.acme_path = os.path.join(os.getcwd(), "acme.sh/acme.sh")

    @property
    def script(self):
        dns_provider_key = self.dns_provider["providerKey"]
        if self.dns_provider["provider"] == "aliyun":
            self.acme_script = f"{self.acme_path} --upgrade && export Ali_Key={dns_provider_key['accessKey']} && export Ali_Secret={dns_provider_key['accessSecret']} && \
                                {self.acme_path} --register-account -m {self.email} --issue --dns dns_ali -d {self.domain} --no-cron --force --cert-home {self.cert_path}"

        if self.dns_provider["provider"] == "cloudFlare":
            self.acme_script = f"{self.acme_path} --upgrade && export CF_Key={dns_provider_key['CF_Key']} && export CF_Email={dns_provider_key['CF_Email']} && \
                                {self.acme_path} --register-account -m {self.email} --issue --dns dns_cf -d {self.domain} --no-cron --force --cert-home {self.cert_path}"

        if self.dns_provider["provider"] == "dnsPod":
            self.acme_script = f"{self.acme_path} --upgrade && export DP_Id={dns_provider_key['DP_Id']} && export DP_Key={dns_provider_key['DP_Key']} && \
                                {self.acme_path} --register-account -m {self.email} --issue --dns dns_dp -d {self.domain} --no-cron --force --cert-home {self.cert_path}"

        if self.dns_provider["provider"] == "huawei":
            self.acme_script = f"{self.acme_path} --upgrade && export HUAWEICLOUD_Username={dns_provider_key['HUAWEICLOUD_Username']} && \
                                export HUAWEICLOUD_Password={dns_provider_key['HUAWEICLOUD_Password']} && export HUAWEICLOUD_ProjectID={dns_provider_key['HUAWEICLOUD_ProjectID']} &&\
                                {self.acme_path} --register-account -m {self.email} --issue --dns dns_huaweicloud -d {self.domain} --no-cron --force --cert-home {self.cert_path}"

        return self.acme_script
