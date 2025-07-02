#!/usr/bin/env python
# test_email.py - Place in project root

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

import django
django.setup()

from django.core.mail import send_mail
from decouple import config

# Email test with error handling
try:
    send_mail(
        subject='Test from Django',
        message='If you see this, email is working!',
        from_email=config('EMAIL_HOST_USER'),
        recipient_list=[config('ADMIN_EMAIL')],
        fail_silently=False
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {str(e)}")
    print("Check:")
    print("1. .env file exists with correct values")
    print("2. App password is valid")
    print("3. Less secure apps enabled in Gmail")
