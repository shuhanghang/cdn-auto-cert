import asyncio
import dns.asyncresolver
from dns.resolver import NoAnswer
from retry import retry
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt

from configs import *
from log import logger
from .type import CheckedCnameModel

resolve_cname: list[CheckedCnameModel] = []


class CheckCnameFailed(Exception):
    def __str__(self):
        return "检测失败"


@retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(2), retry_error_callback=lambda retry_state: "")
async def check(domain: CheckedCnameModel):
    my_resolver = dns.asyncresolver.Resolver()
    my_resolver.nameservers = PUBLIC_DNS
    domain_name = domain.normalDns
    cname = domain.Cname
    type = domain.type
    try:
        resolve_res = await asyncio.wait_for(my_resolver.resolve(domain_name, "CNAME"), timeout=10)
        for i in resolve_res.response.answer:
            for j in i.items:
                if cname == j.to_text()[:-1]:
                    resolve_cname.append(
                        CheckedCnameModel.model_validate(domain))
                    logger.info(
                        f"{type}: {domain.domainName} 正在作为加速域名使用, Cname: {cname}, SslProtocol: {domain.SslProtocol}, 检查通过")
                else:
                    logger.warning(
                        f"{type}: 检查域名 {domain.checkDomain} CNAME值 !== {cname}")
                    raise CheckCnameFailed

    except NoAnswer:
        logger.warning(f"{type}: 检查域名 {domain.checkDomain} CNAME值 !== {cname}")
        raise CheckCnameFailed

    except Exception as e:
        logger.warning(f"{type}: 检查域名 {domain.checkDomain} 检测失败, error: {e}")


async def async_cname_check(cdn_domains: list[CheckedCnameModel]):
    task_list = []
    for cdn_domain in cdn_domains:
        task_list.append(check(cdn_domain))
    await asyncio.gather(*task_list)


def cdn_cname_check(cdn_domains: list[CheckedCnameModel]) -> list[CheckedCnameModel]:
    """异步检查cdn供应商加速域名cname
    """
    try:
        asyncio.run(async_cname_check(cdn_domains))
    except Exception as e:
        raise e
    finally:
        return resolve_cname
