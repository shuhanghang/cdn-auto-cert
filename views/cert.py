import json

from flask import Blueprint, jsonify, request

from views.utils.auth import auth
from model.db import db, SSlOnline
from core import help_cert_handler, run_cdn_cert_job
from utils.checker.type import CdnDomainModel
from utils.cdn_handler.cdn_handler import CdnConfigHandler
from utils.cdn_handler.type import ProviderCdnModel, ProviderDnsModel
from utils.cdn_handler.cdn_parser import get_dns_provider


cert_bp = Blueprint("cert_bp", __name__)

@cert_bp.route('/update', methods=['POST'])
@auth.login_required
def update():
    data = json.loads(request.data)
    cdn_type = data['cdn_type']
    cdn_provider_name = cdn_type.split('_')[0]
    domain = data['domain']
    dns_provider_name = get_dns_provider(domain)
    ssl = db.session.query(SSlOnline).filter(SSlOnline.domain == domain, SSlOnline.cdn_type == cdn_type).first()
    ssl.cert_status = True
    db.session.commit()
    try:
        dns_provider = ProviderDnsModel.model_validate(
            {'provider': dns_provider_name, 'domains': [domain]})
        cdn_provider = ProviderCdnModel.model_validate(
            {'cdnProvider': cdn_provider_name, 'dns': [dns_provider]})
        cdn_domain = CdnDomainModel.model_validate(
            {'domainName': domain, 'normalDns': domain, 'checkDomain': domain, 'type': cdn_type})
        help_cert_handler(CdnConfigHandler(cdn_provider), [cdn_domain])
        cert_res = run_cdn_cert_job()
        if cert_res:
            return jsonify({'msg': cert_res, 'code': 5000}) 
        return jsonify({'msg': '', 'code': 2000})
    except Exception as e:
        return jsonify({'msg': e, 'code': 5000})
    finally:
        ssl.cert_status = False
        db.session.commit()
