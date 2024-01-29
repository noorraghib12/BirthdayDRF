from django.contrib import admin
from accounts.views import *
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)





urlpatterns = [
    path('register/',RegisterAPI.as_view()),
    path('login/',LoginView.as_view()),
    path('google_login/',GoogleLoginView.as_view())
]
