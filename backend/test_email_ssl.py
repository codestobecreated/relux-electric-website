import os
import django
import sys

# Setup django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

# Override settings for SSL test
settings.EMAIL_PORT = 465
settings.EMAIL_USE_SSL = True
settings.EMAIL_USE_TLS = False

print("Trying to send email via SSL...")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"SSL: {settings.EMAIL_USE_SSL}")
print(f"Password length: {len(settings.EMAIL_HOST_PASSWORD)}")
print(f"To: {settings.ADMIN_TO}")

try:
    recipient_list = settings.ADMIN_TO if isinstance(settings.ADMIN_TO, list) else [settings.ADMIN_TO]
    send_mail(
        subject="Test Django Email (SSL)",
        message="This is a test email from the Relux Electric application setup via SSL.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print("SUCCESS! Email sent successfully via SSL.")
except Exception as e:
    print("FAILED!")
    import traceback
    traceback.print_exc()
