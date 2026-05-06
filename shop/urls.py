from django.urls import path
from shop.views import (
    ShopCreateView,
    ShopUpdateView,
    ShopDetailView,
    UserShopListView,
    AllShops,
)

urlpatterns = [
    path('create/', ShopCreateView.as_view(), name="shop-create"),
    path('update/<uuid:id>/', ShopUpdateView.as_view(), name="shop-update"),
    path('<uuid:id>/', ShopDetailView.as_view(), name='shop_detail'),
    path('<str:username>/', UserShopListView.as_view(), name="shop-list"),
    path('', AllShops.as_view(), name="all-shops"),
]
