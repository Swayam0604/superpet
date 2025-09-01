from django.db import models
from autoslug import AutoSlugField


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(null=False,max_length=100)
    category_slug = AutoSlugField(populate_from='category_name',unique=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='products',default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True)
    product_brand = models.CharField(null=False,default="superpet",max_length=60)
 
    def __str__(self):
        return self.product_name