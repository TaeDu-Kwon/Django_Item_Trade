from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct, ProductImage
from .serializers import GameSerializer, ProductSerializer, AccountProductSerializer, ItemProductSerializer, GameMoneyProductSerializer, ProductImageSerializer
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
            user_id = request.data.get("seller")
            seller = User.objects.get(pk = int(user_id))

            game_id = request.data.get("game")
            game = Game.objects.get(pk = int(game_id))
            product_serializer = serializer.save(seller=seller, game = game)
            
            images = request.FILES.getlist('product_image')

            if len(images) > 0:
                for image in images:
                    if product_type == "account":
                        ProductImage.objects.create(account_product = product_serializer, product_image = image)
                    elif product_type == "item":
                        ProductImage.objects.create(item_product = product_serializer, product_image = image)
                    elif product_type == "game_money":
                        ProductImage.objects.create(game_money_product = product_serializer, product_image = image)

            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 상품 get / update / delete 는 viewsets 사용

class ProductViewsets(viewsets.ModelViewSet):
    
    def get_recently_create_item(self, request, *args, **kwargs):
        # 매인 페이지 최신 아이템 정보
        account_products = AccountProduct.objects.order_by("-created_at")[:5]
        item_products = ItemProduct.objects.order_by("-created_at")[:5]
        game_money_products = GameMoneyProduct.objects.order_by("-created_at")[:5]

        context = {"view_type": "read"}
        account_serializer = AccountProductSerializer(account_products, many = True, context=context)
        item_serializer = ItemProductSerializer(item_products, many = True, context=context)
        game_money_serializer = GameMoneyProductSerializer(game_money_products, many = True, context=context)

        return Response({
            "account_data" : account_serializer.data,
            "item_data" : item_serializer.data,
            "game_money_data" : game_money_serializer.data
        },status=status.HTTP_200_OK)

    def get_product_info(self,request, *args, **kwargs):
        # 상품 상세 페이지지
        product_id = kwargs.get("product_id")
        product_type = kwargs.get("product_type")

        if product_type == "account":
            account_product = AccountProduct.objects.filter(pk=product_id)
            images = ProductImage.objects.filter(account_product = product_id)

            serializer = AccountProductSerializer(account_product, many = True)
            images_serializer = ProductImageSerializer(images, many=True)

        elif product_type == "item":
            item_product = ItemProduct.objects.filter(pk = product_id)
            images = ProductImage.objects.filter(item_product = product_id)

            serializer = ItemProductSerializer(item_product, many = True)
            images_serializer = ProductImageSerializer(images, many=True)

        elif product_type == "game_money":
            game_money_product = GameMoneyProduct.objects.filter(pk = product_id)
            serializer = GameMoneyProductSerializer(game_money_product, many = True)

            images = ProductImage.objects.filter(game_money_product = product_id)
            images_serializer = ProductImageSerializer(images, many=True)
        else:
            return
        
        return Response({
            "product_data" : serializer.data,
            "image_data" : images_serializer.data,
        }, status=status.HTTP_200_OK)
    