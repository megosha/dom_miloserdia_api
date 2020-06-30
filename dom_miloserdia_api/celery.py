import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dom_miloserdia_api.settings')

app = Celery('dom_miloserdia_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = 'default'