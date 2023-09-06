
from pydantic import BaseModel


class CdnDomainModel(BaseModel):
    domainName: str = ''
    SslProtocol: str = ''
    Cname: str = ''
    DomainStatus: str = ''
    normalDns: str = ''
    type: str
    checkDomain: str

CheckedCnameModel = CdnDomainModel
