from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, SmallInteger, Integer
from datetime import datetime

db = SQLAlchemy()

class SSlOnline(db.Model):
    __tablename__  =  "ssl_online"
    id = db.Column(Integer, primary_key=True)
    domain = db.Column(String, nullable=False)
    issuer = db.Column(String)
    cdn_type = db.Column(String)
    validity_days = db.Column(SmallInteger)
    days_left = db.Column(SmallInteger)
    tcp_port = db.Column(SmallInteger)
    cert_exp = db.Column(Boolean)
    ssl_status = db.Column(Boolean, default=False, comment="检测状态")
    cert_status = db.Column(Boolean, default=False, comment="证书更新状态")
    create_date = db.Column(DateTime, onupdate=datetime.now, default=datetime.now)


