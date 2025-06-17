# products/urls.py
from django.urls import path
from . import views

app_name = 'products'  # Namespace for URLs

urlpatterns = [
    path('', views.home, name='home'),
    path('product/all', views.product_list, name='product_list'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]