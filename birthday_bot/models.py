from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField
# Create your models here.



class Events(models.Model):
    date=models.DateField()
    event_en=models.TextField()
    event_bn=models.TextField()
    vector=VectorField(dimensions=1536)

class UserQuery(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    relation= models.CharField(max_length=200)
    question=models.TextField()
    answer=models.TextField(default=None)

    def __repr__(self):
        return f"Email:{self.user.email} [Question:{self.question}]" 



    

