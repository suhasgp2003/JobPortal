from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(message):
    send_mail("Contact Us Form From CareerNest.", message,
              settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
