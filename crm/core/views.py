from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from core.forms import SignUpForm, LoginForm 

# Create your views here.

def index(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/site/')
            else:
                messages.error(request, 'Incorrect email or password.')
        else:
            form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)

def register(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            messages.success(request, 'Account created successfully.')
            return redirect('register')
        else:
            form = SignUpForm()
            messages.error(request, 'There was a problem in account creation.')
    
    context ={
        'form': form
    }
    return render(request, 'registration/register.html', context)

@login_required(login_url='/') 
def site(request):
    return render(request, 'main/index.html', {})


def logout_user(request):
    form = LoginForm()
    logout(request)
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong in password resetting.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })