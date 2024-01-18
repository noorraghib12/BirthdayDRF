
from django.contrib.auth import authenticate
from accounts.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response




def register_social_user(provider, email):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        
        registered_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))

        if not registered_user:
            raise  AuthenticationFailed("Invalid Credentials or AuthProvider !")

        return {
            'message': "Login Successful!",
            'email': registered_user.email,
            'tokens': registered_user.tokens()}

        
    else:
        user = {
            'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'tokens': new_user.tokens()
        }