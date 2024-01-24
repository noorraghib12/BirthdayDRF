from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import auth



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['email','password']



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()
    password_confirm=serializers.CharField()
    def validate(self,data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email is taken')
        elif data['password']!=data['password_confirm']:
            raise serializers.ValidationError('Passwords did not match!')
        else:
            return data
            
    def create(self,validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password_confirm']
        )
        return validated_data




class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()


    def validate(self,data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(f"Account not found.")
        return data
    
    def get_jwt_token(self,data):
        user = auth.authenticate(email=data['email'],password=data['password'])
        if not user:
            return {'message':"Invalid Credentials",'data':{}}
        
        refresh=RefreshToken.for_user(user)
        return  {
            'messsage':'Login Success!',
            'data':{
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }
            }

