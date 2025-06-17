from django.urls import path
from . import views


app_name = 'vendors'


urlpatterns = [
    path('business/', views.business_registration, name='business'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]