from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    role = forms.ChoiceField(label='Role', choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
    