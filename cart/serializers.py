from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_id = serializers.UUIDField(source="product.id", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    price = serializers.DecimalField(
        source="product.final_price", max_digits=12, decimal_places=2, read_only=True
    )
    total_price = serializers.DecimalField(
        source="get_total_price", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_title",
            "product_image",
            "price",
            "quantity",
            "total_price",
            "product_id",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_amount = serializers.DecimalField(
        source="get_cart_total_amount", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_amount",
        ]
