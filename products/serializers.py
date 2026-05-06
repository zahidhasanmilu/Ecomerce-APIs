from rest_framework import serializers
from .models import Category, Product

#--------------- Category List Serializer ---------------#
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "description",
            "is_active",
        ]

#--------------- Product List Serializer ---------------#
class ProductListSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    shop_name = serializers.CharField(source="shop.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "price",
            "discount_percentage",
            "final_price",
            "stock",
            "is_active",
            "shop_name",
            "category_name",
        ]

#--------------- Product Create Serializer ---------------#
class ProductCreateSerializer(serializers.ModelSerializer):
    shop = serializers.CharField(source='shop.owner.id', read_only=True)
    total_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, source='final_price', read_only=True
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'discount_percentage',
            'stock',
            'is_active',
            'shop',
            'category',
            'total_price',
            'image',
        ]
        read_only_fields = ['id', 'total_price', 'shop']
