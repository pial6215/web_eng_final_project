from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import SignUpForm  

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! Please login.')
            return redirect('login')
    else:
        form = SignUpForm()
    
    # Render korar somoy form-ta pathiye dichhi
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=u_name, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {u_name}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
            
    # Sothik path ensure korun
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')