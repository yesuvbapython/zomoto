from django.shortcuts import render, redirect
from .forms import customeUserForm  # consider renaming to CustomUserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import customeVendorForm  
from django.contrib import auth
def registerVendor(request):
    if request.method == "POST":
        form = customeUserForm(request.POST)
        v_form = customeVendorForm(request.POST,request.FILES)
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

            messages.success(request, "Vendor has been created successfully......")
            return redirect('registerVendor')
        else:
            # ⬇️ Return the form with errors to the template
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
            messages.success(request,"Registered successfully......")
            return redirect('registerUser')

    else:
        form = customeUserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST('username')
        password = request.POST('password')
        user = auth.authenticate(username,password)
        if not user:
            messages.error("Invalid credentials.....")
            return redirect('login')
        else:
            auth.login(user=user)
            return redirect('dashboard')
    return render(request,'accounts/login.html')
def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out......")
    return redirect('login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')