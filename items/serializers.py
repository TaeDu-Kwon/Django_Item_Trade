from rest_framework import serializers
from .models import Game, Product, AccountProduct, ItemProduct, GameMoneyProduct

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

    class Meta:
        model = AccountProduct
        fields = '__all__'

class ItemProductSerializer(ProductSerializer):
    item_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price_per_item = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = ItemProduct
        fields = '__all__'

class GameMoneyProductSerializer(ProductSerializer):
    total_amount = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        model = GameMoneyProduct
        fields = '__all__'