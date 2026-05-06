from django.urls import path
from .views import (
    CategoryListAPIView,
    CategoryProductListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path(
        'categories/<int:id>/',
        CategoryProductListAPIView.as_view(),
        name='category-product-list',
    ),
    path('', ProductListAPIView.as_view(), name="product-list"),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='product_details'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
]
