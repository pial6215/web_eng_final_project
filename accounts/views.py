from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        # Ekhane amra form theke data nibo (Pore form banabo, ekhon just basic)
        messages.success(request, 'Signup successful! Please login.')
        return redirect('login') # Successful hole login page-e jabe
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        # Login validation logic pore ashbe
        messages.success(request, 'Logged in successfully!')
        return redirect('home')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        # Form theke data gulo dhora hochhe
        u_name = request.POST.get('username')
        e_mail = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        # Password duto same kina check kora
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')
        
        # Ei username e age theke keu ache kina check kora
        if CustomUser.objects.filter(username=u_name).exists():
            messages.error(request, 'Username already taken! Try another.')
            return redirect('signup')

        # Notun User toiri kora ebong Save kora
        user = CustomUser.objects.create_user(username=u_name, email=e_mail, password=pass1)
        user.save()
        
        messages.success(request, 'Signup successful! Please login.')
        return redirect('login') # Sign up holei login page e niye jabe
        
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        # Form theke username ar password dhora
        u_name = request.POST.get('username')
        pass1 = request.POST.get('password')

        # User Database e ache kina khuje ber kora
        user = authenticate(request, username=u_name, password=pass1)

        if user is not None:
            login(request, user) # Sothik hole login koro
            return redirect('home') # Login hoye gele home page e jabe
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')