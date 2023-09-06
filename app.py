from flask import Flask, render_template
from sqlalchemy import or_
from model.db import db, SSlOnline
from views.utils.tasks import scheduler
from views.utils.auth import auth

from views import ssl_bp, cert_bp


class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = "ieeR9vVXT8yx59RphswDuZgo497Mi86w"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    with app.app_context():
        db.create_all()
        db.session.query(SSlOnline).filter(or_(SSlOnline.ssl_status == True, SSlOnline.cert_status == True)).update(
            {SSlOnline.ssl_status: False, SSlOnline.cert_status: False})
        db.session.commit()
    app.register_blueprint(ssl_bp, url_prefix='/api/v1/ssl/')
    app.register_blueprint(cert_bp, url_prefix='/api/v1/cert/')
    return app


app = create_app()


@app.route("/")
@auth.login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
