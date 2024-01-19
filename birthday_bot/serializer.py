from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# from .manager import UserManager 
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import os
from BirthdayDRF import settings
from PyPDF2 import PdfReader
from rest_framework import serializers

def get_upload_path(filename):
    return os.path.join(settings.STATIC_URL,"uploads",filename)     


class UploadSerializer(serializers.Serializer):
    file=serializers.FileField()

    def get_save_path(self,data):
        filename=data.get('file').name
        return get_upload_path(filename)


    def validate(self,data):
        f_path= self.get_save_path(data)
        if os.path.exists(f_path):
            raise serializers.ValidationError("Sorry, this file already exists in upload directory. Please try again with a different filename.")
        else:
            return data

    def create(self,validated_data):
        f_path = get_upload_path(get_save_path(validated_data))
        validated_data.get('file').save(f_path)
        return validated_data






