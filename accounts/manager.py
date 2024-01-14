from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migration=True



    def create_user(self,username,email,password=None, **extra_fields):
        """
        Register user with given username, email and password with email verification functionality
        """
        if not email:
            raise ValueError("Email is required")
        username=username
        email= self.normalize_email(email)
        user = self.model(username = username,email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self,username, email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        username=username
        user = self.model(username = username,email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user