from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer


# -------------Add Cart Item View----------------#
class CartItemAddView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity < 1:
            raise ValidationError("Quantity must be at least 1")

        product = get_object_or_404(Product, id=product_id, is_active=True)

        # Check if product already in cart
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            return Response({"message": "Product already in cart"}, status=400)

        # Create new CartItem
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity
        )

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=201)


# -------------Update Cart Item View----------------#
class CartItemUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def patch(self, request, *args, **kwargs):
        item = self.get_object()
        quantity = int(request.data.get("quantity", item.quantity))

        if quantity < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        cart = item.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# -------------Change Cart Item Quantity View----------------#
class CartItemQuantityChangeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    lookup_url_kwarg = "id"

    def patch(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_id = kwargs.get("id")
        action = request.data.get("action")  # "increment" বা "decrement"

        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == "increment":
            item.quantity += 1
        elif action == "decrement":
            item.quantity -= 1
        else:
            return Response({"error": "Invalid action"}, status=400)

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


# -------------Delete Cart Item View----------------#
class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product_name = instance.product.title
        self.perform_destroy(instance)

        return Response(
            {"message": f"{product_name} successfully has been removed from the cart."},
            status=status.HTTP_200_OK,
        )


# -------------Cart Detail View----------------#
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()

        if not cart.items.exists():
            return Response(
                {"message": "Cart is empty", "items": [], "total_amount": 0},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


# -------------Delete Cart View----------------#
class CartDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def perform_destroy(self, instance):
        # CartItem remove
        instance.items.all().delete()
