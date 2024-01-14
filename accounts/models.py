from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager 
import datetime
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}



class User(AbstractUser):
    email = models.EmailField(unique=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }





# class ForgetPassword(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE)
#     forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.user.email