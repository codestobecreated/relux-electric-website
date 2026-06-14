import os
import django
import sys

# Setup django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Trying to send email...")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
print(f"Password length: {len(settings.EMAIL_HOST_PASSWORD)}")
print(f"To: {settings.ADMIN_TO}")

try:
    recipient_list = settings.ADMIN_TO if isinstance(settings.ADMIN_TO, list) else [settings.ADMIN_TO]
    send_mail(
        subject="Test Django Email",
        message="This is a test email from the Relux Electric application setup.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print("SUCCESS! Email sent successfully.")
except Exception as e:
    print("FAILED!")
    import traceback
    traceback.print_exc()
