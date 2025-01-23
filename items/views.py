from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct, ProductImage, PurchaseRecord
from .serializers import GameSerializer, ProductSerializer, AccountProductSerializer, ItemProductSerializer, GameMoneyProductSerializer, ProductImageSerializer, PurchaseRecordSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json

from users.models import UserCredit
from users.serializers import UserCreditSerializer

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
        account_products = self.get_recent_products(AccountProduct)
        item_products = self.get_recent_products(ItemProduct)
        game_money_products = self.get_recent_products(GameMoneyProduct)

        context = {"view_type": "read"}
        account_serializer = AccountProductSerializer(account_products, many = True, context=context)
        item_serializer = ItemProductSerializer(item_products, many = True, context=context)
        game_money_serializer = GameMoneyProductSerializer(game_money_products, many = True, context=context)

        return Response({
            "account_data" : account_serializer.data,
            "item_data" : item_serializer.data,
            "game_money_data" : game_money_serializer.data
        },status=status.HTTP_200_OK)
    
    def get_recent_products(self,model):
        return model.objects.filter(sold_out=False).order_by("-created_at")[:5]

    def get_product_info(self,request, *args, **kwargs): 
        # 상품 상세 페이지지
        product_id = kwargs.get("product_id")
        product_type = kwargs.get("product_type")
        
        product_model_map = {
            "account" : (AccountProduct, AccountProductSerializer,"account_product"),
            "item" : (ItemProduct, ItemProductSerializer,"item_product"),
            "game_money" : (GameMoneyProduct, GameMoneyProductSerializer,"game_money_product")
        }

        if not product_type in product_model_map:
            return Response({"error": "Invalid product type"}, status=status.HTTP_400_BAD_REQUEST)
        
        model, ser_class, image_field = product_model_map[product_type]

        product = model.objects.filter(pk = product_id)
        serializer = ser_class(product, many= True, context={"view_type":"read"})

        images = ProductImage.objects.filter(**{image_field:product_id}) #field 값이 다르기 때문에 ** 동적으로 필터링을 넣어준다.
        images_serializer = ProductImageSerializer(images, many=True)
        
        return Response({
            "product_data" : serializer.data,
            "image_data" : images_serializer.data,
        }, status=status.HTTP_200_OK)
    
    
    def buy_the_product(self,request,*args,**kwargs):# 상품 구매
        product_id = request.data.get("product_id")
        product_type = request.data.get("product_type")
        user = request.data.get("user_id")
        quantity = 1
        
        if product_type == "account":
            product = get_object_or_404(AccountProduct, id = product_id)
            price = int(str(product.price).split(".00")[0])
        elif product_type == "item":
            product = get_object_or_404(ItemProduct, id = product_id)
            price = int(str(product.price_per_item).split(".00")[0]) # 수량의 곱 으로 계산할 생각
            quantity = product.quantity
        elif product_type == "game_money":
            product = get_object_or_404(GameMoneyProduct, id = product_id)
            price = int(str(product.total_price).split(".00")[0])
        else:
            return Response({"error": "Invalid product type"}, status=status.HTTP_400_BAD_REQUEST)

        user_credit = get_object_or_404(UserCredit, user = user)
  
        if user_credit.credit < price:
            return Response({"error": "Insufficient credit"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_credit.credit -= price
        user_credit.save()

        product.sold_out = True
        product.save()

        PurchaseRecord.objects.create(
            user = User.objects.get(pk = user),
            product_id = product.id,
            product_title = product.title,
            product_type = product.product_type,
            price = price,
            quantity = quantity
        )

        return Response({"success": "Product purchased successfully"}, status=status.HTTP_200_OK)
    
class PurchaseRecordViewset(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseRecord.objects.all()
    serializer_class = PurchaseRecordSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")  
        user = get_object_or_404(User, pk=pk)  
        return self.queryset.filter(user=user)  