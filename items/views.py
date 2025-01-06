from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct
from .serializers import GameSerializer, ProductSerializer, AccountProductSerializer, ItemProductSerializer, GameMoneyProductSerializer
from django.contrib.auth.models import User

# 게임 생성성
class CreateGameView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# 상품 생성은 generics 사용
class CreateProductView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        product_type = request.data.get("product_type")

        if product_type == "account":
            serializer = AccountProductSerializer(data = request.data)
        elif product_type == "item":
            serializer = ItemProductSerializer(data = request.data)
        elif product_type == "game_money":
            serializer = GameMoneyProductSerializer(data = request.data)
        else:
            return Response({"error": "타입이 다르다"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            user_id = self.request.data.get("seller")
            seller = User.objects.get(pk = int(user_id))
            serializer.save(seller=seller)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 상품 get / update / delete 는 viewsets 사용

class ProductViewsets(viewsets.ModelViewSet):
    
    def get_recently_create_item(self, request, *args, **kwargs):
        product_type = kwargs.get("product_type")

        if product_type == "account":
            queryset = AccountProduct
        elif product_type == "item":
            queryset = ItemProduct
        elif product_type == "game_money":
            queryset = GameMoneyProduct
        else:
            return Response({"error":"타입이 다릅니다."},status=status.HTTP_400_BAD_REQUEST)
        
        data = queryset.objects.all().order_by("create_at")[:15]
        return Response(data,status=status.HTTP_200_OK)
