from django.core.mail import EmailMessage
from celery import shared_task
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage

@shared_task()
def email_verification_task(hash, email_address):
    print("Sending Email")
    
    subject = 'Activate Your Healthwise Account'
    message = render_to_string('acc_active_email.html', hash)
    email = EmailMessage(subject, message, to=[email_address])
    email.send()
    
    print("Email Sent")
