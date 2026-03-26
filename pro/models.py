from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class Category(models.Model):
    cat = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Category/',blank=True,null=True)

    def __str__(self):
        return self.cat
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    qunt = models.IntegerField()
    desc = models.CharField(max_length=250)
    img = models.ImageField(upload_to='Prodect/',blank=True,null=True)
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=200)
    key = models.IntegerField()
    
    # Login attempt tracking
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username