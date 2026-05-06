from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, EmailVerification
from .utils import generate_otp

@shared_task
def send_otp_email_task(email, otp, token):
    """
    Send email with OTP and verification link.
    OTP and token are generated in the view to keep them consistent.
    """
    frontend_url = getattr(
        settings,
        "FRONTEND_VERIFY_URL",
        "http://localhost:5173/account/auth/verify-email-link",
    )
    verification_link = f"{frontend_url}/{token}/"

    subject = "Your Email Verification Code"
    message = (
        f"Your OTP: {otp}\n\n"
        f"Click the link below to verify your email:\n{verification_link}\n\n"
        "OTP is valid for 10 minutes.\n"
        "If you did not request this, ignore this email."
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return {"otp": otp, "token": token}