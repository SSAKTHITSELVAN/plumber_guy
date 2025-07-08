# products/urls.py
from django.urls import path
from . import views

app_name = 'products'  # Namespace for URLs

urlpatterns = [
    path('', views.home, name='home'),
    path('product/all', views.product_list, name='product_list'), # For vendors
    path('product/create/', views.create_product, name='create_product'), # For vendors
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # For vendors (with edit/back buttons)
    path('product/view/<int:pk>/', views.user_product_detail, name='user_product_detail'), # For general users
    path('product/update/<int:pk>/', views.update_product, name='update_product'), # For vendors
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'), # For vendors
    path('search/', views.search_results, name='search_results'), # New search results URL
]