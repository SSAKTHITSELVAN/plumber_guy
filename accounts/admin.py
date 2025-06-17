from django.contrib import admin
from .models.customer_profile_model import UserProfile
# Register your models here.

admin.site.register(UserProfile)
