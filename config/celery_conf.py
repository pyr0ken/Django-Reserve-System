from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4
celery_app.conf.timezone = 'Asia/Tehran'
celery_app.conf.beat_schedule = {
    'check_model_task': {
        'task': 'table.tasks.check_and_unavailable_date',
        'schedule': crontab('*/2'),
    },
}
