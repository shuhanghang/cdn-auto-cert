import asyncio
from retry import retry
import dns.asyncresolver
from tenacity import retry, stop_after_attempt, wait_fixed

from config import *
from log import logger

resolve_cname = []


class CheckCnameFailed(Exception):
    def __str__(self):
        return "检测失败"


@retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(2), retry_error_callback=lambda retry_state: "")
async def cname_check(domain):
    my_resolver = dns.asyncresolver.Resolver()
    my_resolver.nameserver = PUBLIC_DNS
    domain_name = domain['normalDns']
    cname = domain['Cname']
    type = domain['type']
    try:
        resolve_res = await asyncio.wait_for(my_resolver.resolve(domain_name, "CNAME"), timeout=10)
        for i in resolve_res.response.answer:
            for j in i.items:
                if cname == j.to_text()[:-1]:
                    resolve_cname.append(domain)
                    logger.info(
                        f"{type}: \"domain: {domain['domainName']} ; cname: {cname} ; https: {domain['SslProtocol']} ; msg: \'cname配置正确\'\"")
                else:
                    logger.warning(
                        f"{type}: \"domain: {domain['fqdn']} ; cname: {cname} ; https: {domain['SslProtocol']} ; msg: \'cname配置错误\'\"")
                    raise CheckCnameFailed

    except dns.asyncresolver.NoAnswer:
        logger.warning(
            f"{type}: \"domain: {domain['fqdn']} ; cname: {cname} ; https: {domain['SslProtocol']} ; msg: \'cname配置错误\'\"")
        raise CheckCnameFailed

    except Exception as e:
        cname = None
        logger.warning(
            f"{type}: \"domain: {domain['fqdn']} ; cname: {cname} ; https: {domain['SslProtocol']} ; msg: \'{e}\'\"")


async def run_async_cname_check(cdn_domains):
    task_list = []
    for cdn_domain in cdn_domains:
        task_list.append(cname_check(cdn_domain))
    await asyncio.gather(*task_list)


def check_cdn_cname(cdn_domains):
    try:
        asyncio.run(run_async_cname_check(cdn_domains))
    except Exception as e:
        logger.error(f"coroutine: 协程执行错误，error: {e}")
        return []
    finally:
        return resolve_cname
