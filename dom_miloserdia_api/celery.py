import os

from celery import Celery

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dom_miloserdia_api.settings')

app = Celery('dom_miloserdia_api')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks(['front'])
app.conf.task_default_queue = 'default'
app.conf.task_ignore_result = True
