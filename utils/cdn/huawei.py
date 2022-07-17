

# from huaweicloudsdkcore.auth.credentials import GlobalCredentials
# from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
# from huaweicloudsdkcore.exceptions import exceptions
# from huaweicloudsdkcdn.v1 import *

# from .provider import CdnProvider

# if __name__ == "__main__":
#     ak = "<YOUR AK>"
#     sk = "<YOUR SK>"

#     credentials = GlobalCredentials(ak, sk) \

#     client = CdnClient.new_builder() \
#         .with_credentials(credentials) \
#         .with_region(CdnRegion.value_of("cn-north-1")) \
#         .build()

#     try:
#         request = UpdateHttpsInfoRequest()
#         forceRedirectConfigForceRedirect = ForceRedirect(
#             switch=1
#         )
#         httpsHttpInfoRequestBody = HttpInfoRequestBody(
#             cert_name="cert-name",
#             https_status=2,
#             certificate="cert-content",
#             private_key="key-content",
#             force_redirect_config=forceRedirectConfigForceRedirect
#         )
#         request.body = HttpInfoRequest(
#             https=httpsHttpInfoRequestBody
#         )
#         response = client.update_https_info(request)
#         print(response)

#     except exceptions.ClientRequestException as e:
#         print(e.status_code)
#         print(e.request_id)
#         print(e.error_code)

# class HuaweiCert(CdnProvider):
#     def __init__(self, cdn_provider_key):
#         self.credentials = GlobalCredentials(cdn_provider_key['ak'], cdn_provider_key['sk'])
#         self.client = CdnClient.new_builder().with_credentials(credentials).with_region(CdnRegion.value_of("cn-north-1")).build()
#         self.name = "huawei_cdn"


#     def get_ssl_cert(self):
#         """获取证书列表
#             return: [{'name': 'test-shuhang-xyz-cert', 'endDate': '2022-07-12', 'id': 7598096}]
#         """
#         try:
#             request = ListDomainsRequest()
#             request.business_type = "web"
#             request.domain_status = "online"
#             request.page_size = 500
#             request.page_number = 1
#             response = self.client.list_domains(request)
#             print(response)
#         except exceptions.ClientRequestException as e:
#             print(e.status_code)
#             print(e.request_id)
#             print(e.error_code)
#             print(e.error_msg)


#     def upload_cert_for_cdn_dcdn(self, domain, cert ,key):
#         """上传证书到 cdn 对应域名下, 并开启https
#         """
#         request = UpdateHttpsInfoRequest()
#         forceRedirectConfigForceRedirect = ForceRedirect(
#             switch=1
#         )
#         httpsHttpInfoRequestBody = HttpInfoRequestBody(
#             cert_name= domain.replace(".", "-")+"-cert",
#             https_status=2,
#             certificate= cert,
#             private_key= key,
#             force_redirect_config=forceRedirectConfigForceRedirect
#         )
#         request.body = HttpInfoRequest(
#             https=httpsHttpInfoRequestBody
#         )
#         response = self.client.update_https_info(request)
#         print(response)


#     def delete_ssl_cert(self):
#         """从证书管理服务中删除证书
#         """
#         pass

#     def get_dns_from_cdn(self):
#         """从cdn域名管理中获取正在被使用的域名
#             return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
#         """
#         return self.cdn_dns_list

#     def get_dns_from_dcdn(self):
#         """从全站加速域名管理中获取正在被使用的域名
#             return: [{'domainName': 'test.test.com', 'SslProtocol': 'on' ...}]
#         """
#         return self.dcdn_dns_list
