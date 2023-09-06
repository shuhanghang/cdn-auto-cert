class CAProvider():
    def __init__(self, dns_provider_name, domain):
        self.ca_name = ''
        self.dns_provider_name = dns_provider_name
        self.domain = domain
        pass

    @property
    def cmd(self):
        """获取脚本命令"""
        return ''


class CAProviderFactory():
    def __init__(self):
        self.instance = {}

    def registry(self, name: str, provider_cls: type[CAProvider]):
        self.instance[name] = provider_cls

    def get(self, name: str) -> type[CAProvider]:
        if instance := self.instance[name]:
            return instance
        return CAProvider
