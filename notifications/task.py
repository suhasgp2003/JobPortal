from .models import Notification
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from accounts.models import User


@shared_task
def send_notification(user_email, title, message):
    user = User.objects.filter(email=user_email).first()
    if user is None:
        return
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user_email])
