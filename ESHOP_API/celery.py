from celery import Celery
import os
app=Celery('ESHOP_API')
os.environ.setdefault('django.confi:settings','ESHOP_API.settings')
app.config_from_object('ESHOP_API')

app.autodiscover_tasks()
