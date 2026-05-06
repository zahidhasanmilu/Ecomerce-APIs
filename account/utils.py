import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import User, EmailVerification


def generate_otp():
    return str(random.randint(100000, 999999))
