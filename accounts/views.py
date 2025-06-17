from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
from .models import UserProfile

# REGISTER VIEW
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Automatically log the user in
            login(request, user)

            # Create an empty profile if not created via signal
            UserProfile.objects.get_or_create(user=user)

            messages.success(request, f'Account created for {username}! Please complete your profile.')
            return redirect('accounts:profile')  # send to profile form
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# DASHBOARD VIEW
@login_required
def dashboard_view(request):
    return render(request, 'registration/dashboard.html')

# PROFILE FORM VIEW

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Check if this is a request to edit profile (via GET parameter)
    edit_mode = request.GET.get('edit', False)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')  # Redirect to display mode
    else:
        form = ProfileForm(instance=profile)
    
    # If it's a new profile (no phone number) or edit mode requested, show form
    if not profile.phone_number or edit_mode:
        return render(request, 'registration/profile_form.html', {'form': form})
    else:
        # Show profile display
        return render(request, 'registration/profile_display.html', {
            'profile': profile,
            'user': request.user
        })