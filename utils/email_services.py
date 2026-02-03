from django.core.mail import send_mail
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

from celery import shared_task
from ESHOP_API import settings

@shared_task
def send_mails(subject,template_name,to,context):
    tags = striptags(template_name)
    message = render_to_string(tags, context)
    from_email = settings.EMAIL_HOST_USER
    send_mail(html_message=message, message=tags, from_email=from_email, recipient_list=[to], subject=subject)



