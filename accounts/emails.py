from django.core.mail import send_mail
from uuid import uuid4
from django.conf import settings
from .models import User
from .serializer import UserSerializer

def send_otp_via_email(email):
    """
    Send verification token to user who has just registered to our API 
    """
    subject = "Your account verification email"
    auth_string = str(uuid4())
    message = f"Your account authentication token is:\n {auth_string}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from, [email])
    user_obj=User.objects.get(email=email)
    user_obj.email_verification_token=auth_string
    user_obj.save()
    