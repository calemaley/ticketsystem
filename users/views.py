from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from .forms import CreateUserForm, UserPasswordResetForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. You can now login')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

def reset_password(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # Pass the request object to form.save()
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('user-login')
    else:
        form = UserPasswordResetForm()
    
    return render(request, 'users/reset_password.html', {'form': form})
