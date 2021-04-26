import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from core.tasks import fetch_all_feed 


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(
        fetch_all_feed.send,
        CronTrigger.from_crontab("* * * * *"),
    )
    try:
        print("running scheduler")
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
