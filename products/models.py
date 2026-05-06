import os
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from shop.models import Shop


# ---------------sanitize filename ---------------#
def sanitize_filename(filename):
    forbidden = '<>:"/\\|?*'
    return filename.translate(str.maketrans({c: "_" for c in forbidden}))


# ---------------generate unique slug ---------------#
def generate_unique_slug(model, base_slug: str) -> str:
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

# ---------------category upload path ---------------#
def category_upload_path(instance, filename):
    return os.path.join("category", instance.name, filename)

# --------------- Category ---------------#
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to=category_upload_path, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# ---------------product upload path ---------------#
def product_upload_path(instance, filename):
    return os.path.join("product", instance.title, filename)

# --------------- Product ---------------#
class Product(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shop_products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(
        upload_to=product_upload_path,
        default="product/product-default.jpg",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["shop"]),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            base_slug = slugify(self.title)
            self.slug = generate_unique_slug(Product, base_slug)
        else:
            old = Product.objects.filter(pk=self.pk).only("title").first()
            if old and old.title != self.title:
                base_slug = slugify(self.title)
                self.slug = generate_unique_slug(Product, base_slug)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        price = self.price or Decimal("0.00")
        discount = self.discount_percentage or Decimal("0.00")
        return (price * (Decimal("1.0") - discount / Decimal("100.0"))).quantize(
            Decimal("0.01")
        )

    @property
    def total_stock(self) -> int:
        return self.stock

    def __str__(self):
        return f"{self.title} ({self.shop.name})"
