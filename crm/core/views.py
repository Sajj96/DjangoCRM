from django.shortcuts import render, redirect, resolve_url, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from .models import CrmUser
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

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': None,
                'email_template_name': 'registration/reset_email.html',
                'subject_template_name': 'registration/reset_subject.txt',
                'request': request,
                'html_email_template_name': None,
            }
            form.save(**opts)
            return redirect('reset_done')
    else:
        form = PasswordResetForm()
    context = {
        'form': form
    }
    return render(request, 'registration/reset_password.html', {
        'form': form
    })

def reset_done(request):
    return render(request, 'registration/reset_done.html', {})


def reset_confirm(request, uidb64 = None,token = None):
    CrmUser = get_user_model()
    token_generator=default_token_generator
    post_reset_redirect = None
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('reset_complete')
    else:
        post_reset_redirect = resolve_url('reset_confirm')
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CrmUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CrmUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('reset_complete')
        else:
            form = SetPasswordForm(user)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }

    return render(request, 'registration/reset_confirm.html', context)

def reset_complete(request):
    return render(request, 'registration/reset_complete.html', {})