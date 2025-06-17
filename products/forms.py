# products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'slug', 
            'description',
            'category',
            'price_retail',
            'price_wholesale',
            'stock_quantity',
            'unit',
            'image_url',
            'is_active',
            'rating',
            'discount_price',
            'min_order_quantity',
            # 'vendor' is EXCLUDED - will be auto-assigned
        ]
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }