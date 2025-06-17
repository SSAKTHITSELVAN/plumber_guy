from django.shortcuts import render, redirect
from .forms import BusinessRegistrationForm
from django.contrib import messages
from vendors.models.business_model import Business
from products.models import Product

def business_registration(request):
    # Check if user already has a business
    if Business.objects.filter(user=request.user).exists():
        messages.error(request, "You already have a registered business.")
        return redirect('vendors:admin_dashboard')

    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            messages.success(request, "Business registered successfully!")
            return redirect('accounts:dashboard')
    else:
        form = BusinessRegistrationForm()

    return render(request, 'vendors/business_register.html', {'form': form})



# @login_required
def admin_dashboard(request):
    """Admin dashboard with vendor's products"""
    try:
        current_vendor = Business.objects.get(user=request.user)
        products = Product.objects.filter(
            vendor=current_vendor,
            is_active=True
        ).order_by('-created_at')
        
        # You can add additional dashboard-specific logic here
        # For example, getting recent products only for dashboard
        recent_products = products[:6]  # Show only first 6 products on dashboard
        
        context = {
            'products': recent_products,  # or use 'products' for all products
            'total_products': products.count(),
            'vendor': current_vendor,
        }
        
    except Business.DoesNotExist:
        products = []
        messages.info(request, 'Create a business profile to manage products.')
        context = {
            'products': products,
            'total_products': 0,
        }
    
    return render(request, 'vendors/admin_dashboard.html', context)
