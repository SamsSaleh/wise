from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegistrationForm
from .models import User
from .tokens import account_activation_token  
from django.utils.encoding import force_str  
from django.utils.http import urlsafe_base64_decode  
from django.http import HttpResponse
from .tasks import email_verification_task
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.tokens import account_activation_token  
import os
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView

# Create your views here.

def login_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    user_login_form = UserLoginForm()

    if request.method == 'POST':
        email = request.POST.get('username')
        raw_password = request.POST.get('password')
        try:
            account = authenticate(username=User.objects.get(email=email).username, password=raw_password)
            if account is not None:
                login(request, account)
                return redirect('home')
        except Exception:
            account = authenticate(username=email, password=raw_password)
            if account is not None:
                login(request, account)
                return redirect('home')   
        messages.error(request, 'Invalid Credentials')
        return render(request, 'accounts/login.html', {'form': user_login_form})
    else:
        return render(request, 'accounts/login.html', {'form': user_login_form})

def signup_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    user_signup_form = UserRegistrationForm()

    if request.method == 'POST':
        user_signup_form = UserRegistrationForm(request.POST)
        if not user_signup_form.is_valid():
            return render(request, 'accounts/signup.html', {'form': user_signup_form})
        
        username = user_signup_form.cleaned_data.get('username')
        email = user_signup_form.cleaned_data.get('email')
        password = user_signup_form.cleaned_data.get('password1')
        role = user_signup_form.cleaned_data.get('role')
        
        try:
            User.objects.get(email=email)
            return render(request, 'accounts/signup.html', {'form': user_signup_form, 'error': 'Email already exists'})
        except Exception:
            pass
        
        try:
            User.objects.get(username=username)
            return render(request, 'accounts/signup.html', {'form': user_signup_form, 'error': 'Username already exists'})
        except Exception:
            pass
        
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        user.is_active = False
        user.save()
        
        email_verification_task.delay({
            'user': user.username,
            'domain': os.environ.get('DOMAIN'),
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        }, email)
        
        return redirect('login')
    
    return render(request, 'accounts/signup.html', {'form': user_signup_form})    
    

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

class MyPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/reset-email-sent/'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

def reset_email_sent(request):
    return HttpResponse('Password reset email sent')

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = '/password_reset_complete/'
