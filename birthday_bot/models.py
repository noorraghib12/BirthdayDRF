from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField
# Create your models here.



class Events(models.Model):
    event_date=models.DateField()
    english_text=models.TextField()
    bengali_text=models.TextField()
    vector=VectorField(dimensions=1536)

class UserQuery(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    relation= models.CharField(max_length=200)
    question=models.TextField()
    answer=models.TextField()

    def __repr__(self):
        return self.user.email



    

