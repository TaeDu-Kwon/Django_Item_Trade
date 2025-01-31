from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart of "+self.user.username
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  
    product_id = models.PositiveBigIntegerField() 
    product_type = models.CharField(max_length=20) 
    title = models.CharField(max_length=150) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    class Meta:
        unique_together = ("cart", "product_id", "product_type")  # 중복 추가 방지

    def __str__(self):
        return f"{self.title} in {self.cart.user.username}'s cart"