from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_order_confirmation_email(order_id,email_id):
    subject="Order Conformation"
    message=f" your order with {order_id} has been confirmed!! congratulations!!"

    return send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email_id])