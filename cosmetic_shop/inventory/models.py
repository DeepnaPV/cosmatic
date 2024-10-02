from django.db import models

# Create your models here.


class products(models.Model):
    category_choice=(
        ('skincare','skincare'),
        ('makeup','makeup'),
        ('hair','hair'),
        ('fragrance', 'Fragrance'),
        ('tools', 'Beauty Tools'),
        ('bath','bath and body'),
    )
    brand=(
        ('Maybelline New York','Maybelline New York'),
        ('Lakme','Lakme'),
        ('Nykaa Cosmetics','Nykaa Cosmetics'),
        ('M.A.C','M.A.C'),
        ('The Face Shop','The Face Shop'),
    )
    name=models.CharField(max_length=60)
    brand=models.CharField(max_length=50,choices=brand)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=category_choice)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class inventordetails(models.Model):
    address=models.TextField()
    pin=models.IntegerField()
    phonenum=models.IntegerField()
    aadharnum=models.IntegerField()
    userimg=models.ImageField(upload_to='inventors')
     





