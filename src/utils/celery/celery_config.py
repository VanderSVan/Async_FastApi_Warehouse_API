from celery import Celery
from src.config import get_settings

settings = get_settings()

app = Celery(__name__, include=['src.utils.celery.celery_tasks'])
app.config_from_object(settings, namespace='CELERY')

# Queues storage if workers are busy
app.conf.broker_url = settings.get_redis_url()

# Backend result storage
app.conf.result_backend = settings.get_redis_url()

app.autodiscover_tasks()
