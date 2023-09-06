from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from auto_cert import auto_cert_service
from configs import AUTO_CERT_CRON

if __name__=="__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(auto_cert_service, CronTrigger.from_crontab(AUTO_CERT_CRON), max_instances=1)
    scheduler.start()
