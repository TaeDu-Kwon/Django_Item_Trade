from rest_framework import serializers
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct, ProductImage, PurchaseRecord
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class AccountProductSerializer(ProductSerializer):
    account_class = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    
    def get_game(self, obj):
        if self.context.get("view_type") == "read":
            return obj.game.name  # 게임 이름 출력
        return obj.game.id  # 기본 ID 반환

    def get_seller(self, obj):
        if self.context.get("view_type") == "read":
            return obj.seller.username  # 판매자 이름 출력
        return obj.seller.id  # 기본 ID 반환

    class Meta:
        model = AccountProduct
        fields = '__all__'    

class ItemProductSerializer(ProductSerializer):
    item_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price_per_item = serializers.DecimalField(max_digits=10, decimal_places=2)

    game = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    
    def get_game(self, obj):
        if self.context.get("view_type") == "read":
            return obj.game.name  # 게임 이름 출력
        return obj.game.id  # 기본 ID 반환

    def get_seller(self, obj):
        if self.context.get("view_type") == "read":
            return obj.seller.username  # 판매자 이름 출력
        return obj.seller.id  # 기본 ID 반환

    class Meta:
        model = ItemProduct
        fields = '__all__'

class GameMoneyProductSerializer(ProductSerializer):
    total_amount = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2)

    game = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    
    def get_game(self, obj):
        if self.context.get("view_type") == "read":
            return obj.game.name  # 게임 이름 출력
        return obj.game.id  # 기본 ID 반환

    def get_seller(self, obj):
        if self.context.get("view_type") == "read":
            return obj.seller.username  # 판매자 이름 출력
        return obj.seller.id  # 기본 ID 반환

    class Meta:
        model = GameMoneyProduct
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class PurchaseRecordSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseRecord
        fields = [
            "id",
            "user",
            "product_title",
            "product_type",
            "price",
            "quantity",
            "purchased_at",
            "product_image",
        ]
    def get_product_image(self, obj):
        # 상품 유형에 따라 이미지를 동적으로 가져오기
        if obj.product_type == "account":
            image = ProductImage.objects.filter(account_product_id=obj.product_id).first()
        elif obj.product_type == "item":
            image = ProductImage.objects.filter(item_product_id=obj.product_id).first()
        elif obj.product_type == "game_money":
            image = ProductImage.objects.filter(game_money_product_id=obj.product_id).first()
        else:
            return None
        
        # 이미지가 존재하면 URL 반환
        return image.product_image.url if image else None