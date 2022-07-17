import os
import time
import random
import subprocess

from tenacity import retry, stop_after_attempt, wait_fixed

from config import *
from log import logger
from .acme import Acme
from utils.notify import send_email
from utils.checker import ssl_check
from utils.cdn.provider import CdnProvider


class CreateCertFailed(Exception):
    pass


class CertManager():
    """证书管理器"""

    def __init__(self, checked_domain: list, dns_provider_config: dict, cdn_provider: CdnProvider):
        self.dns_provider = dns_provider_config
        self.cdn_provider = cdn_provider
        self.checked_domain = checked_domain
        self.domain = ""
        self.days_left = ""

    def run(self):
        """管理器入口"""
        logger.info(
            f"{self.checked_domain['type']}: \"domain: {self.checked_domain['domainName']}, 证书剩余过期时间（天）{self.days_left} <= {EXPIRE_MAX} 正在尝试申请并更新... ...\"")
        self.acme_script = Acme(self.dns_provider, self.domain).script
        try:
            if self.acme_script and self.request_cert():
                if self.get_cert():
                    self.post_cert()
        except Exception:
            logger.error(
                f"{self.checked_domain['type']}: \"domain: {self.domain} ; msg: 申请证书失败\"")

    @property
    def check_expire(self):
        """检查证书过期时间"""
        try:
            check_res, legal_domain = ssl_check(self.checked_domain["fqdn"])
            if check_res:
                self.days_left = check_res[legal_domain]["days_left"]
                if self.days_left in CERT_EXPIRE_ALERT and MAIL_ENABLE:  # 证书过期满足报警天数发送报警
                    logger.info(
                        f"{self.checked_domain['type']}: \"domain: {self.checked_domain['domainName']} ; msg: 过期天数为 {self.days_left} 触发报警\"")
                    send_email(
                        self.dns_provider['provider'], self.checked_domain, self.days_left)
                if EXPIRE_MIN <= self.days_left <= EXPIRE_MAX:  # 证书过期满足期望值重新申请证书
                    self.domain = self.checked_domain["normalDns"]
                    return True
        except Exception as e:
            logger.warning(
                f"{self.checked_domain['type']}: \"domain: {self.checked_domain['domainName']} ; msg: {e}\"")
            return False

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(5))
    def request_cert(self):
        """申请证书"""
        acme_server = random.choice(ACME_CERT_SERVER)
        acme_script = self.acme_script + f" --server {acme_server}"
        process = subprocess.Popen(
            acme_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        command_output = process.stdout.read().decode('utf-8')
        logger.info(
            f"acme.sh: \"domain: {self.domain}\" ; ca: {acme_server} ; msg:")
        print(command_output)
        if process.returncode == 0:
            return True
        else:
            raise CreateCertFailed

    def get_cert(self):
        """获取证书"""
        base_path = f"/{ACME_CERT_PATH}/{self.domain}"
        cert_path = os.path.join(base_path, "fullchain.cer")
        key_path = os.path.join(base_path, self.domain + ".key")
        if os.path.exists(cert_path) and os.path.exists(key_path):
            if time.time() - os.stat(cert_path).st_mtime < 60*10:
                with open(cert_path, "r") as cert:
                    self.cert_file = cert.read()
                with open(key_path, "r") as key:
                    self.key_file = key.read()
                if self.cert_file and self.key_file:
                    return True
        else:
            logger.error(
                f"{self.checked_domain['type']}: \"domain: {self.checked_domain['domainName']} ; msg: 申请的证书文件不存, 请检查路径 {base_path}\"")
            return False

    def post_cert(self):
        """上传证书"""
        self.cdn_provider.upload_cert_to_cdn(
            self.checked_domain['domainName'], self.cert_file, self.key_file)
