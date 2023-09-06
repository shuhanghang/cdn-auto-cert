import json
from flask import request, Blueprint, jsonify

from model.db import db
from model.db import SSlOnline
from views.utils.auth import auth
from utils.checker import ssl_check
from utils.checker.type import CheckedCnameModel
from core import check_cdn_all_cname, check_cdn_dns_health
from configs import cert_handler_list

ssl_bp = Blueprint('ssl_bp', __name__)


@ssl_bp.route("/list")
@auth.login_required
def ssl_list():
    """加速域名证书信息"""
    if cdn_type := request.args.get('cdn_type'):
       cdn_name = cdn_type.split('_')[0]
       data = db.session.query(SSlOnline).filter(SSlOnline.cdn_type.ilike(f"%{cdn_name}%")).filter_by()
    elif domain := request.args.get('domain'):
       data = db.session.query(SSlOnline).filter(SSlOnline.domain.ilike(f"%{domain}%")).filter_by()
    else:
       data = db.session.query(SSlOnline).filter_by()
    page_data = data.paginate(
        page=int(request.args.get("page", 1)),
        per_page=int(request.args.get("limit", 10)),
        error_out=False,
        max_per_page=50
    ).items
    data_list = []
    for i in page_data:
        data_list.append({
            "id": i.id,
            "domain": i.domain,
            "issuer": i.issuer,
            "cdn_type": i.cdn_type,
            "expire": str(i.days_left) + '/' + str(i.validity_days),
            "progress": i.days_left/i.validity_days*100,
            "cert_exp": i.cert_exp,
            'ssl_status': i.ssl_status,
            'cert_status': i.cert_status,
            "create_time": i.create_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    res = {'code': 0, 'count': len(data.all()), 'data': data_list}
    return res

@ssl_bp.route("/check", methods=['POST'])
@auth.login_required
def check_ssl():
    """检查加速域名"""
    data = json.loads(request.data)
    domain = data['domain']
    cdn_type = data['cdn_type']
    checked_domain = CheckedCnameModel.model_validate(
        {'checkDomain': domain, 'type': cdn_type})
    ssl = db.session.query(SSlOnline).filter(
        SSlOnline.domain == domain, SSlOnline.cdn_type == checked_domain.type).first()
    ssl.ssl_status = True
    db.session.commit()
    check_res, _ = ssl_check(checked_domain)
    ssl.ssl_status = False
    db.session.commit()
    if check_res and ssl:
        res_ssl = {
            "id": ssl.id,
            "domain": ssl.domain,
            "issuer": ssl.issuer,
            "cdn_type": ssl.cdn_type,
            "expire": str(ssl.days_left) + '/' + str(ssl.validity_days),
            "progress": ssl.days_left/ssl.validity_days*100,
            "cert_exp": ssl.cert_exp,
            "create_time": ssl.create_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify({'data': res_ssl, 'code':2000})
    return jsonify({'data': {}, 'code': 5000})


@ssl_bp.route("/update", methods=['POST'])
@auth.login_required
def update_ssl():
    check_cdn_all_cname()
    check_cdn_dns_health()
    cert_handler_list.clear
    return {'code': 2000}