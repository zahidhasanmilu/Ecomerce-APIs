from django.contrib import admin
from .models import Category, Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'shop',
        'shop__owner__email',
        'category',
        'price',
        'discount_percentage',
        'final_price',
        'stock',
        'is_active',
    )
    readonly_fields = ('final_price', 'created_at', 'updated_at')
    list_filter = ('shop', 'category', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
