from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Products=models.ManyToManyField(Product,through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True,default=0)

class Order(models.Model):
    order_id = models.CharField(max_length=15,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ManyToManyField(Product,through='OrderItem')
    address_line_1=models.CharField(max_length=40,null=False)
    address_line_2=models.CharField(max_length=40,null=False)
    city=models.CharField(max_length=40,null=False)
    state=models.CharField(max_length=40,null=False)
    pin_code=models.PositiveIntegerField(null=False)
    phone_no=models.CharField(max_length=10,null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True,default=0)
