from rest_framework import serializers
from .models import Cart, CartItem
from django.contrib.auth.models import User

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, read_only=True) 

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']  # 사용자와 생성 날짜는 자동 처리
    