from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager 
import datetime


class User(AbstractUser):
    username=models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    credit = models.FloatField()
    address = models.CharField(max_length=1000,blank=True)
    profileimg = models.ImageField(upload_to='profile_images')


    def __str__(self):
        return self.user.email




# class ForgetPassword(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE)
#     forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.user.email