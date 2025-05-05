from django.shortcuts import render, redirect
from .forms import customeUserForm  # consider renaming to CustomUserForm
from .models import User
from django.contrib import messages
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
