from django import forms
from items.models import Game

class ProductForm(forms.Form):
    PRODUCT_TYPE_CHOICES = [
        ('account', "Account"),
        ('item', "Item"),
        ('game_money', "Game Money"),
    ]
    product_type = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES, label="Product Type")
    game = forms.ModelChoiceField(queryset=Game.objects.all(), label="Game")
    title = forms.CharField(max_length=150, label="Title")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")

    # AccountProduct 전용 필드
    account_class = forms.CharField(max_length=30, required=False, label="Account Class")
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Price")

    # ItemProduct 전용 필드
    item_name = forms.CharField(max_length=100, required=False, label="Item Name")
    quantity = forms.IntegerField(required=False, label="Quantity")
    price_per_item = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Price per Item")

    # GameMoneyProduct 전용 필드
    total_amount = forms.IntegerField(required=False, label="Total Amount")
    total_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Total Price")
