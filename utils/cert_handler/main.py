
import os
import sys
import subprocess

from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt

from configs import *
from log import logger
from utils.checker import ssl_check
from utils.alert import send_notification
from utils.cdn_providers.provider import CdnProvider
from utils.cdn_handler.type import ProviderDnsModel
from utils.checker.type import CheckedCnameModel
from utils.ca_providers import ca_providers, CAProvider
from utils.cdn_handler.cdn_parser import get_ca_provider


class CreateCertFailed(Exception):
    """生成证书重试失败"""

    def __str__(self):
        return "生成证书重试失败"


class CertHandler():
    """证书处理器"""

    def __init__(self, checked_domain: CheckedCnameModel, dns_provider_config: ProviderDnsModel, cdn_provider: CdnProvider):
        """
        Args
            checked_domains (CheckedCnameModel): cdn上正在使用且已canme检查后的域名
            dns_provider_config (ProviderDnsModel): dns_provider配置
            cdn_provider (CdnProvider): cdn供应商对象
        """
        self.dns_provider_config = dns_provider_config
        self.cdn_provider = cdn_provider
        self.dns_provider_name = dns_provider_config.provider
        self.domains = checked_domain
        self.domain = checked_domain.normalDns
        self.cdn_type = checked_domain.type
        self.ca_provider: CAProvider
        self.days_left = ''
        self.alert = ALERT

    def apply_cert(self):
        """申请证书并上传到CDN
        """
        try:
            self.handle_cdn_cert()
        except Exception:
            logger.warning(
                f"{self.domains.type}: {self.ca_provider.ca_name}使用域名 {self.domain} 申请证书失败")
            return "申请证书失败"
        try:
            self.read_cdn_cert()
        except Exception:
            logger.warning(
                f"{self.domains.type}: {self.ca_provider.ca_name}使用域名 {self.domain} 上传证书失败")
            return "上传证书失败"

    @property
    def check_cert_online(self):
        """检查证书过期时间
        """
        check_res, legal_domain = ssl_check(self.domains)
        if check_res:
            self.days_left = check_res[legal_domain]["days_left"]
            if self.days_left in CERT_EXPIRE_ALERT and self.alert:  # 证书过期满足报警天数发送报警
                logger.info(
                    f"{self.domains.type}: 加速域名 {self.domains.domainName} 过期天数为 {self.days_left} 触发报警")
                send_notification(self.dns_provider_name,
                                  self.domains, self.days_left)
            if EXPIRE_MIN <= self.days_left <= EXPIRE_MAX:  # 证书过期满足期望值重新申请证书
                logger.info(
                    f"{self.domains.type}: 加速域名为 {self.domains.domainName} 证书剩余过期时间（天）{self.days_left} <= {EXPIRE_MAX} 正在尝试申请并更新...")
                return True

    def _run_lego(self) -> int:
        process = subprocess.Popen(self.ca_provider.cmd, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                                   stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
        process.communicate()
        return process.returncode

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(5))
    def handle_cdn_cert(self):
        """生成证书"""
        cdn_provider_name = self.cdn_type.split('_')[0]
        ca_provider_name = get_ca_provider(
            cdn_provider_name, self.dns_provider_config.provider)
        ca_provider_class = ca_providers.get(ca_provider_name)
        self.ca_provider = ca_provider_class(
            self.dns_provider_name, self.domain)
        logger.info(f"{self.ca_provider.ca_name}: 域名·{self.domain}·的证书申请详情:\n")
        if not self._run_lego():
            return
        else:
            logger.error(
                f"{self.ca_provider.ca_name}: 域名·{self.domain}·的证书申请失败，正在重试...\n")
            raise CreateCertFailed

    def read_cdn_cert(self):
        """读取证书"""
        cert_path = os.path.join(
            CERT_PATH, "certificates", self.domain + ".crt")
        key_path = os.path.join(
            CERT_PATH, "certificates", self.domain + ".key")
        with open(cert_path, "r") as cert, open(key_path, "r") as key:
            self.cert_file = cert.read()
            self.key_file = key.read()
        if self.cert_file and self.key_file:
            self.upload_to_cdn_provider()

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(5))
    def upload_to_cdn_provider(self):
        """上传证书"""
        try:
            self.cdn_provider.upload_cert_for_cdn(
                self.domains.domainName, self.cert_file, self.key_file)
        except Exception as e:
            logger.error(f"{self.domains.type}: 上传证书失败，详情：{e}")
            raise Exception("上传证书失败")
