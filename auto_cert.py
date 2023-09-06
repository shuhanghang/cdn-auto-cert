
from log import logger
from core import run_cdn_cert_job, check_cdn_all_cname, check_cdn_dns_health


def auto_cert_service():
    check_cdn_all_cname()
    check_cdn_dns_health()
    run_cdn_cert_job()
    logger.info("cdn-auto-cert: 执行完成")

if __name__ == "__main__":
    auto_cert_service()
