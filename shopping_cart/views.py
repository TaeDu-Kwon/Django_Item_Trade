from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        # 현재 로그인한 사용자에 대한 장바구니만 반환
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 장바구니는 각 사용자마다 하나만 생성
        if not Cart.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # 로그인한 사용자의 장바구니 아이템만 반환
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        user = get_object_or_404(User, id = user_id)
        cart, created = Cart.objects.get_or_create(user=user)  # 장바구니 생성 또는 가져오기
        data = request.data.copy()
        data['cart'] = cart.id  # 요청 데이터에 장바구니 ID 추가
        
        existing_item = CartItem.objects.filter(cart = cart, product_id=data['product_id'], product_type=data['product_type']).first()

        if existing_item:
            return Response({"detail": "Item already exists in the cart."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        product_id = kwargs.get("product_id")
        product_type = kwargs.get("product_type")

        user = get_object_or_404(User,id = user_id)
        cart = get_object_or_404(Cart,user=user)

        cart_item = CartItem.objects.filter(cart=cart,product_id = product_id,product_type = product_type).first()
        cart_item.delete()

        return Response({"detail": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
