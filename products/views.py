from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from shop.permissions import IsOwnerOrReadOnly, IsShopOwnerRole

from .models import Category, Product
from .serializers import (
    CategoryListSerializer,
    ProductListSerializer,
    ProductCreateSerializer,
)
from shop.paginations import CustomPagination


# --------------- Category List ---------------- #
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    # pagination_class = CustomPagination


# --------------- Category Products List ---------------- #
class CategoryProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        category_id = self.kwargs.get("id")
        return Product.objects.filter(
            category__id=category_id, is_active=True, shop__status="active"
        )


# --------------- All Products List ---------------- #
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True, category__is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


# --------------- Product Detail ---------------- #
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True, category__is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_object(self):
        product_id = self.kwargs.get("id")
        product = Product.objects.filter(
            is_active=True, category__is_active=True, id=product_id
        ).first()
        if not product:
            raise NotFound(
                detail={"message": "Product not found", "product_id": product_id}
            )
        return product


# --------------- Product Create ---------------- #
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsShopOwnerRole]

    def perform_create(self, serializer):
        shop = self.request.user.shops.filter(status="active").first()
        serializer.save(shop=shop)
