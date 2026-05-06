from django.urls import path
from .views import (
    CartDetailView,
    CartItemAddView,
    CartItemUpdateView,
    CartItemDeleteView,
    CartItemQuantityChangeView,
    CartDeleteView,
)

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/add/", CartItemAddView.as_view(), name="cart-item-add"),
    path(
        "items/update/<int:id>/", CartItemUpdateView.as_view(), name="cart-item-update"
    ),
    path(
        "items/delete/<int:id>/", CartItemDeleteView.as_view(), name="cart-item-delete"
    ),
    path(
        "items/change-quantity/<int:id>/",
        CartItemQuantityChangeView.as_view(),
        name="cart-item-change-quantity",
    ),
    path("delete/", CartDeleteView.as_view(), name="cart-delete"),
]
