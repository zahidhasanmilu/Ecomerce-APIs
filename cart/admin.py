from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_cart_total_amount', 'created_at')
    search_fields = ('user__email',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_total_price')
    search_fields = ('cart__user__email', 'product__title')


# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
