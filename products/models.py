# products/models.py
from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price_retail = models.DecimalField(max_digits=10, decimal_places=2)
    price_wholesale = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500)
    
    # Optional Advanced Fields
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_order_quantity = models.IntegerField(default=1)
    
    # Fixed relationship with vendor - Direct import
    vendor = models.ForeignKey('vendors.Business', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name