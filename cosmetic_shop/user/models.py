from django.db import models
from inventory.models import products
from django.contrib.auth.models import User

# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def get_subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"

    def __str__(self):
        return self.user.username
    
    
