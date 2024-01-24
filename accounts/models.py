from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager 
import datetime


class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    access_token = models.CharField(max_length=200 ,blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    

    def __str__(self):
        return self.email



# class ForgetPassword(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE)
#     forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.user.email