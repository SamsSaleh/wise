from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not password:
            raise ValueError('Password is required')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('role', 'health_expert')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('health_expert', 'Health Expert')
    )
    
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    username = models.CharField(max_length=255, verbose_name='username', unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id}: {self.username}'
