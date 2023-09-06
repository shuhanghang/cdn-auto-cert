from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger

from model.db import db, SSlOnline
from auto_cert import auto_cert_service
from configs import AUTO_CERT_CRON


scheduler = APScheduler()


@scheduler.task(trigger=CronTrigger.from_crontab(AUTO_CERT_CRON), misfire_grace_time=900, max_instances=1)
def aut_cert_service_job():
    with scheduler.app.app_context():
        db.session.query(SSlOnline).delete()
        db.session.commit()
        auto_cert_service()
