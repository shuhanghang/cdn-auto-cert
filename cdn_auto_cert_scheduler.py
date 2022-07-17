from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from utils.core.controller import main
from config import AUTO_CERT_CRON

if __name__=="__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(main, CronTrigger.from_crontab(AUTO_CERT_CRON), max_instances=1)
    scheduler.start()
