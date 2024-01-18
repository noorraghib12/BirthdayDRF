from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField
# Create your models here.


class UserQuery(models.Model):
    event_date=models.DateField()
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    relation= models.CharField(max_length=200)
    question=models.TextField()
    answer=models.CharField()
    vectors=VectorField(dimensions=1536)
    
    def __repr__(self):
        return self.user.email



    

