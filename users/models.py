from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.credit}"