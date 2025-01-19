from rest_framework import serializers
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct, ProductImage
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