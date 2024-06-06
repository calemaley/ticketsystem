from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserPasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form=CreateUserForm()
    context = {
        'form':form,
    }
    return render(request, 'user/register.html',context)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def reset_password(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # Pass the request object to form.save()
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('user-login')
    else:
        form = UserPasswordResetForm()
    
    return render(request, 'user/reset_password.html', {'form': form})
