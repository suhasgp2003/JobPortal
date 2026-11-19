from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import User


@shared_task
def send_email_otp(OTP, to_email):
    subject = "Email Verification OTP"
    message = (
        f"Your One-Time Password (OTP) for email verification is {OTP}.\n\n"
        f"This OTP is valid for a limited time. Please do not share it with anyone."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


@shared_task
def send_sms(OTP, to_no):
    body = (
        f"Your OTP for verification is {OTP}. "
        f"It is valid for a limited time. Do not share it with anyone."
    )
    if not (settings.TWILIO_SID and settings.TWILIO_AUTH and settings.TWILIO_FROM_NO):
        print(f"\n[SMS to {to_no}] {body}\n")
        return
    from twilio.rest import Client
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)
    client.messages.create(body=body, from_=settings.TWILIO_FROM_NO, to=to_no.replace(" ", ''))


@shared_task
def delete_user(email, phone_no):
    user = User.objects.filter(email=email, phone_no=phone_no).first()
    if user is None:
        return
    if user.user_type == 'candidate' and not user.candidate.is_verified:
        user.delete()
    elif user.user_type == 'company' and not user.company.otp_verified:
        user.delete()
