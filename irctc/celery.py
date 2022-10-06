# path/to/your/proj/src/cfehome/celery.py
import os
from celery import Celery
from django.apps import apps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irctc.settings')

app = Celery('irctc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
