from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ilovePython, 'cron', second=2)
    scheduler.start()


def ilovePython():
    print("I love python {}".format(datetime.now()))
