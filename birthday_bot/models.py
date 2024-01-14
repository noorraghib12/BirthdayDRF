from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserQuery(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.TextField()
    Answer=models.CharField(max_length=150)
    
    def __repr__(self):
        return self.user.email
    

