# vendors/views.py
from django.shortcuts import render, redirect
from .forms import BusinessRegistrationForm
from django.contrib import messages
from vendors.models.business_model import Business
from products.models import Product
from leads.models import Lead  # Import Lead model
from django.contrib.auth.decorators import login_required

@login_required
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


def admin_dashboard(request):
    """
    Admin dashboard with vendor's products and ALL LEADS from the platform
    """
    try:
        current_vendor = Business.objects.get(user=request.user)
        products = Product.objects.filter(
            vendor=current_vendor,
            is_active=True
        ).order_by('-created_at')
        
        # Get recent products for dashboard
        recent_products = products[:6]  # Show only first 6 products on dashboard
        
        # GET ALL LEADS from the platform (visible to all vendors)
        all_leads = Lead.objects.all().select_related('user', 'product', 'product__vendor').order_by('-timestamp')
        
        # You can also filter leads by date range if needed
        # from datetime import timedelta
        # from django.utils import timezone
        # recent_leads = all_leads.filter(timestamp__gte=timezone.now() - timedelta(days=30))
        
        context = {
            'products': recent_products,
            'total_products': products.count(),
            'vendor': current_vendor,
            'leads': all_leads,  # All leads visible to all vendors
            'total_leads': all_leads.count(),
        }
        
    except Business.DoesNotExist:
        products = []
        all_leads = Lead.objects.all().select_related('user', 'product', 'product__vendor').order_by('-timestamp')
        
        messages.info(request, 'Create a business profile to manage products.')
        context = {
            'products': products,
            'total_products': 0,
            'leads': all_leads,  # Still show leads even without business profile
            'total_leads': all_leads.count(),
        }
    
    return render(request, 'vendors/admin_dashboard.html', context)


@login_required
def leads_view(request):
    """
    Dedicated view for showing all leads (can be used for a separate leads page)
    """
    try:
        current_vendor = Business.objects.get(user=request.user)
        
        # Get all leads from the platform
        all_leads = Lead.objects.all().select_related('user', 'product', 'product__vendor').order_by('-timestamp')
        
        # Optional: Add filtering capabilities
        # You can add filters like date range, product category, etc.
        
        context = {
            'leads': all_leads,
            'total_leads': all_leads.count(),
            'vendor': current_vendor,
        }
        
    except Business.DoesNotExist:
        messages.error(request, 'Business profile required to view leads.')
        return redirect('vendors:business_registration')
    
    return render(request, 'vendors/leads.html', context)