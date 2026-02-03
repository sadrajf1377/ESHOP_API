from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','ESHOP_API.settings')

celery_app=Celery('ESHOP_API')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

