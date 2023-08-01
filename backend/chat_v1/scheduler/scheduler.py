from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from chat_v1.models import Message


def clear_db():
    """Удаление старых сообщений."""
    Message.objects.filter(
        sending_datetime__lte=datetime.now()
        - timedelta(seconds=settings.CLEAR_DB_TIME_SECONDS)
    ).delete()


def start():
    """Основная логика создания тасок на чистку БД."""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        clear_db,
        trigger=CronTrigger(hour=settings.CLEAR_DB_TIME_HRS),
        id="clear_db",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
