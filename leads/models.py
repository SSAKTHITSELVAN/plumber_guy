from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Lead model
class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} viewed {self.product.name} at {self.timestamp}"
