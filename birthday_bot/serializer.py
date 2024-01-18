from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager 
import datetime
from rest_framework_simplejwt.tokens import RefreshToken






class UploadSerializer(serializers.Serializer):
    file=serializers.FileField()