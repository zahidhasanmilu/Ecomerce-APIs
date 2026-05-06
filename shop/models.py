import os
import uuid
from django.db import models
from django.utils.text import slugify
from account.models import User


#--------------- Sanitize filename ---------------#
def sanitize_filename(filename):
    forbidden = '<>:"/\\|?*'
    return filename.translate(str.maketrans({c: "_" for c in forbidden}))


#--------------- Safe email for path ---------------#
def safe_email(email):
    return email.replace("@", "_at_").replace(".", "_")

#--------------- Generate unique slug ---------------#
def generate_unique_slug(model, base_slug):
    slug = base_slug
    counter = 1

    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

#--------------- Upload path for shop logo ---------------#
def shop_logo_upload_to(instance, filename):
    filename = sanitize_filename(filename)
    owner = instance.owner

    role = getattr(owner, "role", "default")
    email = safe_email(owner.email)
    shop_name = slugify(instance.name)

    return os.path.join("user_profile", role, email, shop_name, "logo", filename)


# 5. Upload path for cover image
def shop_cover_upload_to(instance, filename):
    filename = sanitize_filename(filename)
    owner = instance.owner

    role = getattr(owner, "role", "default")
    email = safe_email(owner.email)
    shop_name = slugify(instance.name)

    return os.path.join("user_profile", role, email, shop_name, "cover", filename)


class Shop(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("disabled", "Disabled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="shops", on_delete=models.CASCADE)

    # BASIC DETAILS
    name = models.CharField(max_length=255, unique=True)

    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    # IMAGES
    logo = models.ImageField(upload_to=shop_logo_upload_to, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to=shop_cover_upload_to, blank=True, null=True
    )

    # CONTACT INFO
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=32, blank=True)
    address = models.TextField(blank=True)

    # EXTRA SETTINGS
    policies = models.JSONField(blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)

    # STATUS
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    is_verified = models.BooleanField(default=False)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
