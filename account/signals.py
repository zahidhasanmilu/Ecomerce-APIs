from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, EmailVerification
from .utils import generate_otp
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=User)
def post_user_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()
