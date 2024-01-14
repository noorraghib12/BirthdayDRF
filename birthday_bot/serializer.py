from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import auth


