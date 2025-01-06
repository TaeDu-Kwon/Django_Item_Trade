from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('account',"Account"),
        ('item',"Item"),
        ('game_money','Game Money')
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # 어떤 게임인지
    title = models.CharField(max_length=150) # 제목
    seller = models.ForeignKey(User, on_delete=models.CASCADE) # 판매자
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES) # 판매품 종류
    description = models.TextField(blank=True, null=True) # 설명
    created_at = models.DateTimeField(auto_created=True,null=True) # 생성 날짜

    class Meta: 
        # 추상 모델 ( 실제 데이터베이스 테이블로 생성되지 않는 기반 클래스 주로 공통 필드와 메서드를 다른 모델에서 재사용하기 위해서 정의한다. )
        abstract = True

class AccountProduct(Product):
    account_class = models.CharField(max_length=30) # 계정 직업
    price = models.DecimalField(max_digits=10, decimal_places=2) # 계정 가격

    def __str__(self):
        return f"{self.product_type} - {self.game}"

class ItemProduct(Product):
    item_name = models.CharField(max_length=100) # 아이템 이름
    quantity = models.PositiveIntegerField() # 수량
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2) # 개당 가격

    def __str__(self):
        return f"{self.product_type} - {self.item_name}"

class GameMoneyProduct(Product):
    total_amount = models.PositiveIntegerField() # 판매 할 총 게임머니
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # 총 가격

    def __str__(self):
        return f"{self.product_type} - {self.game}"