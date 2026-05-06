from products.models import Product
from account.models import User
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def get_cart_total_amount(self):
        total = 0
        for item in self.items.all():
            total += item.product.final_price * item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"

    @property
    def get_total_price(self):
        return self.product.final_price * self.quantity
