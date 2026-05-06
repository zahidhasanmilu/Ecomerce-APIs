# account/emails.py
from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(verification):
    verify_link = (
        f"{settings.FRONTEND_URL}/account/auth/verify-email-link/{verification.token}"
    )

    message = f"""
Your OTP: {verification.otp}

Click the link below to verify your email:
{verify_link}

OTP is valid for 10 minutes.
"""

    send_mail(
        subject="Verify your email",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[verification.user.email],
        fail_silently=False,
    )
