# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from .forms import ProductForm
from vendors.models.business_model import Business
from leads.models import Lead
from django.utils import timezone
from django.db.models import Q # Import Q object for complex queries

def home(request):
    """
    Renders the home page with all active products from all vendors.
    """
    # Get all active products from all vendors
    products = Product.objects.filter(is_active=True).select_related('vendor').order_by('-created_at')

    return render(request, 'products/home.html', {
        'products': products
    })

@login_required
def create_product(request):
    """Create product and auto-assign to logged-in user's business"""

    # Get the current user's business/vendor
    try:
        current_vendor = Business.objects.get(user=request.user)
    except Business.DoesNotExist:
        messages.error(request, 'You must have a business profile to create products.')
        return redirect('vendor_profile')  # Redirect to create business profile

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Don't save yet - we need to assign vendor
            product = form.save(commit=False)
            product.vendor = current_vendor  # Auto-assign current vendor
            product.save()
            form.save_m2m()  # Save many-to-many relationships (tags)

            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('vendors:admin_dashboard')
    else:
        form = ProductForm()

    return render(request, 'products/create_product.html', {
        'form': form,
        'current_vendor': current_vendor
    })

@login_required
def product_list(request):
    """List products for current vendor only"""
    try:
        current_vendor = Business.objects.get(user=request.user)
        products = Product.objects.filter(
            vendor=current_vendor,
            is_active=True
        ).order_by('-created_at')
    except Business.DoesNotExist:
        products = []
        messages.info(request, 'Create a business profile to manage products.')

    return render(request, 'products/product_list.html', {
        'products': products
    })

def product_detail(request, pk):
    """
    View single product for VENDOR and CREATE LEAD when user views details
    """
    product = get_object_or_404(Product, pk=pk)

    # CREATE LEAD: Track when user views product details
    if request.user.is_authenticated:
        # Check if lead already exists for this user+product combination
        # to avoid duplicate leads (optional - remove if you want multiple leads)
        lead, created = Lead.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'timestamp': timezone.now()}
        )

        if created:
            print(f"New lead created: {request.user} viewed {product.name}")
    else:
        # For anonymous users, still create lead but without user
        Lead.objects.create(
            user=None,  # Anonymous user
            product=product
        )
        print(f"Anonymous lead created for product: {product.name}")

    return render(request, 'products/product_detail.html', {
        'product': product
    })

def user_product_detail(request, pk):
    """
    View single product for general USER. Create LEAD ONLY if user is authenticated.
    """
    product = get_object_or_404(Product, pk=pk)

    # CREATE LEAD: Track when user views product details, ONLY if authenticated
    if request.user.is_authenticated:
        # Check if lead already exists for this user+product combination
        lead, created = Lead.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'timestamp': timezone.now()}
        )

        if created:
            print(f"New lead created: {request.user} viewed {product.name}")
    # Removed the else block that created leads for anonymous users.

    return render(request, 'products/user_product_detail.html', { # Note the new template name
        'product': product
    })

# New view for handling search results
def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.none() # Initialize an empty queryset

    if query:
        # Filter active products by name or description (case-insensitive)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        ).order_by('-created_at')

    # Pass the query to the template for display, even if no results
    return render(request, 'products/search_results.html', {
        'query': query,
        'products': products
    })


@login_required
def update_product(request, pk):
    """Update product - only if owned by current vendor"""
    product = get_object_or_404(Product, pk=pk)

    # Security check - only vendor who owns product can edit
    try:
        current_vendor = Business.objects.get(user=request.user)
        if product.vendor != current_vendor:
            messages.error(request, 'You can only edit your own products.')
            return redirect('products:product_list')
    except Business.DoesNotExist:
        messages.error(request, 'Business profile required.')
        return redirect('vendor_profile')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/update_product.html', {
        'form': form,
        'product': product
    })

@login_required
def delete_product(request, pk):
    """Delete product - only if owned by current vendor"""
    product = get_object_or_404(Product, pk=pk)

    # Security check
    try:
        current_vendor = Business.objects.get(user=request.user)
        if product.vendor != current_vendor:
            messages.error(request, 'You can only delete your own products.')
            return redirect('products:product_list')
    except Business.DoesNotExist:
        messages.error(request, 'Business profile required.')
        return redirect('vendor_profile')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('products:product_list')

    return render(request, 'products/delete_product.html', {
        'product': product
    })

# --- Custom template filters (add this section) ---
# Create a templatetags directory inside your 'products' app
# e.g., products/templatetags/products_extras.py
# And then load it in your templates: {% load products_extras %}

# For quick testing, you can add a simple filter directly here,
# but it's best practice to put it in a separate templatetags file.
# If you don't want to create a separate file for this one filter,
# you can calculate price_saved in the view and pass it.

# Here's how you'd define it in a templatetags file:
# from django import template
# register = template.Library()
# @register.filter
# def sub(value, arg):
#     return value - arg