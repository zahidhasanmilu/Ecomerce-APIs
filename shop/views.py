from rest_framework import generics, permissions
from shop.permissions import IsOwnerOrReadOnly, IsShopOwnerRole
from django.shortcuts import get_object_or_404
from account.models import User
from shop.paginations import CustomPagination

from .models import Shop
from .serializers import (
    ShopCreateSerializer,
    ShopUpdateSerializer,
    ShopDetailSerializer,
    ShopsListSerializer,
)

# ---------------- ALL SHOPS LIST (Public) ---------------- #
class AllShops(generics.ListAPIView):
    serializer_class = ShopsListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Shop.objects.filter(status="active").order_by("-created_at")


# ---------------- USER SHOP LIST ---------------- #
class UserShopListView(generics.ListAPIView):
    serializer_class = ShopDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        return Shop.objects.filter(owner=user, status="active").order_by("-created_at")


# ---------------- SHOP DETAIL ---------------- #
class ShopDetailView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailSerializer
    lookup_field = 'id'


# ---------------- CREATE SHOP ---------------- #
class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwnerRole]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ---------------- UPDATE SHOP ---------------- #
class ShopUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = ShopUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwnerRole]
    queryset = Shop.objects.all()
    lookup_field = 'id'
