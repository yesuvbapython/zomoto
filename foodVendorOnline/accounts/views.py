from django.shortcuts import render, redirect
from .forms import customeUserForm  # Consider renaming to CustomUserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import customeVendorForm
from django.contrib import auth
from .utils import dashboard
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import send_verification_mail_to_activate
from django.core.exceptions import PermissionDenied

def customer_role(user):
    if user.role == 1:
        return True
    raise PermissionDenied

def vendore_role(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def registerVendor(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('login')
    
    if request.method == "POST":
        form = customeUserForm(request.POST)
        v_form = customeVendorForm(request.POST, request.FILES)
        
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            send_verification_mail_to_activate(request,vendor)                            
            messages.success(request, "Vendor has been created successfully.")
            return redirect('registerVendor')
        else:
            print(form.errors)
            print(v_form.errors)
            context = {
                'form': form,
                'v_form': v_form
            }
            return render(request, 'accounts/registerVendor.html', context)
    
    else:
        form = customeUserForm()
        v_form = customeVendorForm()
        context = {
            'form': form,
            'v_form': v_form
        }
        return render(request, 'accounts/registerVendor.html', context)

def registerUser(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('login')
    
    if request.method == "POST":
        form = customeUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.role = User.CUSTOMER
            user.save()
            send_verification_mail_to_activate(request,user)
            messages.success(request, "Registered successfully.")
            return redirect('registerUser')
        else:
            print(form.errors)
            return render(request, 'accounts/registerUser.html', {'form': form})
    
    else:
        form = customeUserForm()
        return render(request, 'accounts/registerUser.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('login')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        
        if not user:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
        else:
            auth.login(request, user=user)
            messages.success(request, "You are logged in.")
            print('Logged in')
            return redirect('Account')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out.")
    return redirect('login')

@login_required(login_url='login')
def Account(request):
    print("Hello world!!!!!")
    user = request.user
    reDirect = dashboard(user)
    return redirect(reDirect)

@login_required(login_url='login')
@user_passes_test(customer_role)
def cusDashboard(request):
    return render(request, 'accounts/cusDashboard.html')

@login_required(login_url='login')
@user_passes_test(vendore_role)
def venDashboard(request):
    return render(request, 'accounts/venDashboard.html')

def activate(request):
    pass
